        package com.creditrisk.backend.controller;

import com.creditrisk.backend.model.PredictionRequest;
import com.creditrisk.backend.model.PredictionResponse;
import com.creditrisk.backend.service.PredictionService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class PredictionController {

    private final PredictionService predictionService;

    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @GetMapping("/health")
    public ResponseEntity<String> health(Authentication authentication) {
        return ResponseEntity.ok()
                .header("X-User-Role", authentication == null ? "" : authentication.getAuthorities().stream()
                        .findFirst().map(authority -> authority.getAuthority().replace("ROLE_", "")).orElse(""))
                .body("OK");
    }

    @GetMapping("/model-info")
    public String modelInfo() {
        return "XGBoost v1.0.0 - Credit Risk Model";
    }

    @PostMapping("/predict")
    public PredictionResponse predict(@Valid @RequestBody PredictionRequest request) {
        return predictionService.predict(request.getFeatures());
    }

    @GetMapping("/history")
    public List<Map<String, Object>> history(
            @RequestParam(defaultValue = "20") int limit,
            @RequestParam(defaultValue = "own") String scope) {
        return predictionService.history("all".equalsIgnoreCase(scope), limit);
    }

    @GetMapping("/metrics")
    public Map<String, Object> metrics() {
        return predictionService.metrics();
    }
}