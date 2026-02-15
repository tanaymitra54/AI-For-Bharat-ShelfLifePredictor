# Requirements Specification

## 1. Scope
This document defines functional and non-functional requirements for the AI Food Shelf Life Predictor web application, aligned for AWS AI for Bharat hackathon submission.

## 2. Stakeholders
- End users seeking shelf-life guidance.
- Developers maintaining model, API, and frontend.
- Project owners evaluating system accuracy and usability.

## 3. Functional Requirements
- FR-1: The system must accept input fields: `food_type`, `storage_type`, `temperature`, `humidity`, `days_stored`.
- FR-2: The system must return predicted remaining shelf life in days.
- FR-3: The system must classify result status as `Safe`, `Consume Soon`, or `Expired`.
- FR-4: The system must return clear recommendations based on predicted and interpreted risk.
- FR-5: The system must provide human-readable explanation details for each prediction.
- FR-6: The system must expose a health-check endpoint.
- FR-7: The system must support batch prediction requests.
- FR-8: The system should provide voice explanation when ElevenLabs credentials are configured.
- FR-9: The system should provide chat-based assistance when OpenRouter credentials are configured.
- FR-10: The frontend must present prediction, voice, and chat interaction tabs.
- FR-11: The solution must include a demoable Bharat-relevant use case narrative in project documentation.
- FR-12: The system must provide interpretable output (status, rationale, recommendation) suitable for hackathon judging walkthroughs.

## 4. Input and Validation Requirements
- VR-1: `temperature` and `humidity` must be numeric.
- VR-2: `days_stored` must be numeric and non-negative.
- VR-3: `food_type` and `storage_type` must be non-empty known categories.
- VR-4: Invalid payloads must return structured error responses with actionable messages.

## 5. API Requirements
- AR-1: The API must expose `GET /health` and return service status.
- AR-2: The API must expose `POST /predict` for primary inference.
- AR-3: The API must expose `POST /explain` for detailed explanations.
- AR-4: The API must expose `POST /batch_predict` for multiple inputs.
- AR-5: The API must expose chat/voice endpoints as optional capabilities.
- AR-6: API responses must be JSON and include consistent field names.

## 6. Model and Inference Requirements
- MR-1: Inference must include preprocessing and feature engineering before prediction.
- MR-2: Rule-based interpretation must be applied after base ML prediction.
- MR-3: The system should prioritize conservative recommendations under risky conditions.
- MR-4: Model artifacts and preprocessors must be loadable at API startup.

## 7. Non-Functional Requirements
- NFR-1: Prediction endpoint target latency should be under 500 ms in local demo conditions.
- NFR-2: The system should remain available even if optional third-party voice/chat services fail.
- NFR-3: Secrets must be managed through environment variables, never hardcoded.
- NFR-4: The codebase must remain modular (preprocessing, feature engineering, model, rules, services).
- NFR-5: Frontend must support current desktop and mobile browsers commonly used for demos.
- NFR-6: The project should be deployable on AWS services suitable for hackathon demonstration.
- NFR-7: The codebase and docs should be structured for quick evaluator onboarding (under 15 minutes).

## 8. Observability and Error Handling
- OR-1: Backend should log request failures with enough detail for debugging.
- OR-2: User-facing errors should avoid leaking secrets or internal stack traces.
- OR-3: Health endpoint should support quick deployment verification.

## 9. Acceptance Criteria
- AC-1: A valid prediction request returns `200 OK` with days estimate, status class, and recommendations.
- AC-2: Invalid request payload returns `4xx` with field-level validation feedback.
- AC-3: `GET /health` confirms service readiness.
- AC-4: Frontend can trigger prediction and render results without page reload.
- AC-5: If voice/chat keys are configured, corresponding endpoints return successful responses.
- AC-6: Documentation includes architecture summary, setup steps, API endpoint list, and demo flow.
- AC-7: A hackathon reviewer can run the app locally and complete one prediction scenario end-to-end.

## 10. Constraints and Assumptions
- The system provides guidance, not official food safety certification.
- Accuracy depends on training dataset quality and category coverage.
- Voice/chat features depend on third-party API availability and valid credentials.

## 11. AWS AI For Bharat Hackathon Requirements Mapping
- HR-1 (Innovation): Use AI/ML as the core decision mechanism rather than static rule-only logic.
- HR-2 (Impact): Focus on practical Bharat context where food storage guidance can reduce waste.
- HR-3 (Feasibility): Provide a runnable MVP with clear setup and stable core path.
- HR-4 (Explainability): Return human-readable rationale and safety classification with every prediction.
- HR-5 (Demo Quality): Provide coherent UI journey with measurable outputs and clear success criteria.
- HR-6 (Cloud Readiness): Define AWS deployment targets for API, frontend, storage, and monitoring.
- HR-7 (Documentation): Include architecture, requirements, usage steps, and known limitations.
