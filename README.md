<h1 align="center">
  <img width="20%" src="./docs/logo.png" />
  <br />
  Hydrogen
  <br></br>
<p align="center">
<img alt="Blockchain" src="https://img.shields.io/badge/-Blockchain-121D33?style=for-the-badge&logo=blockchain.com&logoColor=white" />
<img alt="Flask" src="https://img.shields.io/badge/-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
</p>
</h1>

A simplified but fundamental implementation of a blockchain node, just like the hydrogen atom is.

## Getting Started

### **Prerequisites**

- Python 3 installed.

### **Running**

1. Make a clone:

```sh
   git clone https://github.com/amintasvrp/hydrogen.git
```

2. Create and use virtual enviroment:

   ```bash
   python -m venv venv
   ```

   2.1. Use host and port by command line
   ```powershell
      .\venv\Scripts\Activate.ps1
   ```
   2.2. Use host and port in ```settings.ini```

   ```bash
      source venv
   ```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Run node:

   4.1. Use host and port by command line

   ```bash
      python src/main.py <host> <port>
   ```
   4.2. Use host and port in ```settings.ini```

   ```bash
      python src/main.py
   ```

### **Contributing**

Make a pull request and make clear what changes have been made and which bugs persist. Do not introduce bugs, be proactive!

## Licenses

- **MIT License** - [_Show details_](./LICENSE)
