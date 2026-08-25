        package com.creditrisk.backend.controller;

import com.creditrisk.backend.model.PredictionRequest;
import com.creditrisk.backend.model.PredictionResponse;
import com.creditrisk.backend.service.PredictionService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PredictionController {

    private final PredictionService predictionService;

    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @GetMapping("/health")
    public String health() {
        return "OK";
    }

    @GetMapping("/model-info")
    public String modelInfo() {
        return "XGBoost v1.0.0 - Credit Risk Model";
    }

    @PostMapping("/predict")
    public PredictionResponse predict(@Valid @RequestBody PredictionRequest request) {
        return predictionService.predict(request.getFeatures());
    }
}