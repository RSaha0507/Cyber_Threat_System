# Cyber Threat Intelligence & Response System (CTIRS)

A real-time, modular cybersecurity monitoring and response platform developed in Python.  
It ingests threat feeds, detects anomalies using intelligent models, visualizes threats through a live dashboard, and sets the foundation for automated incident response.

## Key Features

- **Live Threat Feed Aggregation**  
  Pulls real-time indicators of compromise (IoCs) from platforms like AlienVault OTX (with plans for AbuseIPDB, GreyNoise, etc.).

- **Anomaly Detection Engine** *(Modular)*  
  Supports Isolation Forest, One-Class SVM, and LOF for identifying suspicious patterns in threat data.

- **Real-Time Dashboard with Streamlit**  
  Clean and dynamic UI showing threat summaries, anomaly flags, and performance metrics.

- **Alert & Logging Framework**  
  Planned integration for alerting (email/Slack) and incident response logging.

- **Extensible Design**  
  Fully modular architecture for integrating new feeds, models, and response strategies.

- **SPIN-based Formal Verification** *(Planned)*  
  Intended use of model checking to verify state transitions and system logic.

## Tech Stack

| Layer         | Tools / Libraries                      |
|---------------|----------------------------------------|
| Backend       | Python 3.x, Pandas, PyMongo            |
| Database      | MongoDB (NoSQL)                        |
| Anomaly Models| Scikit-learn, PyOD (planned)           |
| Frontend      | Streamlit                              |
| Profiling     | cProfile, snakeviz                     |
| Testing       | Pytest (unit + integration tests)      |
| Verification  | SPIN (planned)                         |

## Project Structure

cyber_threat_system/
├── aggregator/ # Data fetchers from OTX, etc.
├── db/ # MongoDB connection and config
├── detection/ # Anomaly detection logic
├── response/ # Future incident response modules
├── streamlit_app.py # Dashboard entry point
├── test_integration.py # Integration test suite
├── requirements.txt # Dependency file
├── README.md # You're here :)
└── .gitignore

## Testing & Quality

- **Integration Test Suite:** 5 integration test cases simulate data flow and module interaction.
- **Test Coverage:** 96% overall (100% on test modules, >90% on logic).
- **Code Metrics:**  
  - Cyclomatic complexity: Rated A/B across all modules (low complexity).
  - Maintainability: High
- **Profiling:** Identified bottlenecks in geolocation & DB writes (caching suggested).

## Roadmap

- [x] Integration with AlienVault OTX
- [x] Modular anomaly detection
- [ ] Alerting system (email/Slack)
- [ ] Incident response logging
- [ ] SPIN-based formal verification
- [ ] Extend to GreyNoise / AbuseIPDB feeds

## Contribution

Pull requests are welcome. If you’d like to contribute, please fork the repo and use a feature branch.  
For major changes, open an issue first to discuss what you’d like to change.

## License

This project is currently used for academic or demonstrative purposes.  
Contact the maintainer if you'd like to collaborate or repurpose the architecture.

## Contact

**Rounak Saha**  
🔗 [LinkedIn](https://www.linkedin.com/in/rounak-saha-932ab0253/) | ✉️ rs574.cs008@gmail.com

> “Cybersecurity isn’t just detection—it’s understanding the threat, responding, and learning from it. This platform moves one step closer to making that real-time.”
