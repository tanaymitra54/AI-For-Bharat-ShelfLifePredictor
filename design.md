# Design Document

## 1. Overview
AI Food Shelf Life Predictor is a full-stack system that estimates remaining shelf life based on food type, storage conditions, and elapsed storage time. The system combines machine learning predictions with rule-based interpretation to improve safety-focused outcomes.

## 2. Goals
- Provide fast and reliable shelf life prediction for common food-storage scenarios.
- Return actionable guidance (status, issues, recommendations), not just a numeric estimate.
- Expose a clean API for frontend and external integrations.
- Support explainability through voice and chat interfaces.

## 3. Non-Goals
- Replacing certified food safety testing.
- Handling medical advice or legal compliance guarantees.
- Real-time IoT sensor ingestion in the current version.

## 4. System Architecture
- Frontend: Next.js app with prediction UI, voice tab, and chat assistant tab.
- Backend API: Flask service exposing prediction and assistant endpoints.
- ML Layer: Random Forest model for base shelf-life estimation.
- Rule Layer: Post-processing logic for extreme conditions and safety interpretation.
- Service Integrations: ElevenLabs (voice synthesis), OpenRouter (chat).

## 5. High-Level Data Flow
1. User submits input (`food_type`, `storage_type`, `temperature`, `humidity`, `days_stored`) from frontend.
2. Backend validates request and runs preprocessing.
3. Feature engineering computes derived signals (deviation, interaction, degradation).
4. ML model predicts remaining shelf life.
5. Rule interpreter adjusts prediction and classifies risk (`Safe`, `Consume Soon`, `Expired`).
6. API returns structured response with recommendations and optional explanation context.
7. Voice/chat tabs consume explanation endpoints as needed.

## 6. Core Components
- `backend/src/preprocessing/preprocessor.py`: input cleansing, imputation, encoding, scaling.
- `backend/src/feature_engineering/engineer.py`: derived feature construction.
- `backend/src/models/predictor.py`: model loading and prediction.
- `backend/src/inference/pipeline.py`: orchestration of inference steps.
- `backend/src/rules/interpreter.py`: rule-based adjustment and guidance.
- `backend/src/services/voice_service.py`: ElevenLabs integration.
- `backend/src/services/chat_service.py`: OpenRouter integration.
- `frontend/src/services/api.ts`: frontend API client.
- `frontend/src/hooks/usePrediction.ts`: prediction state and request handling.

## 7. API Design
- `GET /health`: service health.
- `POST /predict`: main prediction result.
- `POST /explain`: richer textual explanation.
- `POST /batch_predict`: multi-item prediction.
- `POST /voice/explain`: audio explanation payload.
- `POST /chat`: food safety and storage Q&A.
- `POST /chat/prediction_explanation`: assistant explanation for a result.
- `POST /chat/storage_advice`: targeted food storage advice.

## 8. Security and Reliability Considerations
- Validate request payload types and ranges before inference.
- Keep external API keys in environment variables only.
- Gracefully degrade when third-party services are unavailable.
- Return explicit error payloads for invalid inputs and downstream failures.

## 9. Performance Targets
- Typical single prediction latency target: under 500 ms on local deployment (excluding external chat/voice calls).
- API should support concurrent user interactions for demo-scale traffic.
- Frontend should display progress/loading states and avoid blocking UI threads.

## 10. Extensibility
- Swap model implementation without changing API contract.
- Add new food/storage categories through retraining and encoder updates.
- Introduce additional explainers (e.g., confidence score) with backward-compatible response fields.

## 11. Deployment Assumptions
- Backend runs as Python service (Flask) on port `5000`.
- Frontend runs as Next.js app on port `3000`.
- Environment variables are configured for optional voice/chat features.
