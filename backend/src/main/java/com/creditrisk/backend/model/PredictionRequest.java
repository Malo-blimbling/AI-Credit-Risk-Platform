package com.creditrisk.backend.model;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.List;

public class PredictionRequest {
    @NotNull(message = "Les features sont obligatoires")
    @Size(min = 35, max = 35, message = "35 features sont nécessaires")
    private List<Double> features;

    public List<Double> getFeatures() { return features; }
    public void setFeatures(List<Double> features) { this.features = features; }
}