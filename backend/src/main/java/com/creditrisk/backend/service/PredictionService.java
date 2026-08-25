package com.creditrisk.backend.service;

import com.creditrisk.backend.model.PredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class PredictionService {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${ml.service.url}")
    private String mlServiceUrl;

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

        return new PredictionResponse(probability, riskScore, riskCategory,
                shapValues, timestamp, "v1.0.0");
    }
}