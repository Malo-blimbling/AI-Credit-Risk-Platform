package com.creditrisk.backend.model;

import java.util.Map;

public class PredictionResponse {
    private double probabilityOfDefault;
    private int riskScore;
    private String riskCategory;
    private Map<String, Double> shapExplanation;
    private String timestamp;
    private String modelVersion;

    public PredictionResponse() {}

    public PredictionResponse(double probabilityOfDefault, int riskScore,
                              String riskCategory, Map<String, Double> shapExplanation,
                              String timestamp, String modelVersion) {
        this.probabilityOfDefault = probabilityOfDefault;
        this.riskScore = riskScore;
        this.riskCategory = riskCategory;
        this.shapExplanation = shapExplanation;
        this.timestamp = timestamp;
        this.modelVersion = modelVersion;
    }

    public double getProbabilityOfDefault() { return probabilityOfDefault; }
    public void setProbabilityOfDefault(double probabilityOfDefault) { this.probabilityOfDefault = probabilityOfDefault; }
    public int getRiskScore() { return riskScore; }
    public void setRiskScore(int riskScore) { this.riskScore = riskScore; }
    public String getRiskCategory() { return riskCategory; }
    public void setRiskCategory(String riskCategory) { this.riskCategory = riskCategory; }
    public Map<String, Double> getShapExplanation() { return shapExplanation; }
    public void setShapExplanation(Map<String, Double> shapExplanation) { this.shapExplanation = shapExplanation; }
    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }
    public String getModelVersion() { return modelVersion; }
    public void setModelVersion(String modelVersion) { this.modelVersion = modelVersion; }
}