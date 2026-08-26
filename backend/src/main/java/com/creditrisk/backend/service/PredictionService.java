package com.creditrisk.backend.service;

import com.creditrisk.backend.model.PredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class PredictionService {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${ml.service.url}")
    private String mlServiceUrl;

    private final List<Map<String, Object>> history = new CopyOnWriteArrayList<>();

    public PredictionResponse predict(List<Double> features) {
        Map<String, Object> request = new HashMap<>();
        request.put("features", features);

        Map<String, Object> response = restTemplate.postForObject(
            mlServiceUrl + "/predict",
            request,
            Map.class
        );

        double probability = (double) response.get("probability");
        int riskScore = (int) response.get("risk_score");
        String riskCategory = (String) response.get("risk_category");
        Map<String, Double> shapValues = (Map<String, Double>) response.get("shap_values");

        String timestamp = LocalDateTime.now()
                .format(DateTimeFormatter.ISO_LOCAL_DATE_TIME);

        PredictionResponse prediction = new PredictionResponse(probability, riskScore, riskCategory,
                shapValues, timestamp, "v1.0.0");
        Map<String, Object> record = new HashMap<>();
        record.put("date", timestamp);
        record.put("clientId", "PRED-" + (history.size() + 1));
        record.put("probabilityOfDefault", probability);
        record.put("riskCategory", riskCategory);
        record.put("decisionStatus", decisionFor(riskCategory));
        history.add(record);
        return prediction;
    }

    public List<Map<String, Object>> history(boolean full, int limit) {
        List<Map<String, Object>> result = new ArrayList<>(history);
        Collections.reverse(result);
        return result.subList(0, Math.min(Math.max(limit, 0), result.size()));
    }

    public Map<String, Object> metrics() {
        long high = history.stream().filter(row -> "HIGH".equals(row.get("riskCategory"))).count();
        long referred = history.stream().filter(row -> "Référée".equals(row.get("decisionStatus"))).count();
        double average = history.stream()
                .mapToDouble(row -> ((Number) row.get("probabilityOfDefault")).doubleValue())
                .average().orElse(0);
        Map<String, Object> result = new HashMap<>();
        result.put("total", history.size());
        result.put("avg_default", average);
        result.put("pct_high", history.isEmpty() ? 0 : (double) high / history.size());
        result.put("referred", referred);
        result.put("rocAuc", null);
        result.put("brierScore", null);
        result.put("confusionMatrix", List.of(List.of(0, 0), List.of(0, 0)));
        result.put("shapGlobal", Map.of());
        result.put("timeline", List.of());
        return result;
    }

    private String decisionFor(String category) {
        return switch (category) {
            case "LOW" -> "Acceptée";
            case "MEDIUM" -> "Référée";
            default -> "Refusée";
        };
    }
}