# SDV GUI with KUKSA Databroker

This project provides a Python-based vehicle dashboard GUI built with **PySide6**.  
It communicates with the **Eclipse KUKSA Databroker** via gRPC and is designed to run on a **Raspberry Pi 5 (64-bit)**.

The GUI can read vehicle signals, send control signals, and interact with other interfaces using a custom VSS definition.

---

## System Requirements

- Raspberry Pi 5
- Raspberry Pi OS 64-bit (Bookworm recommended)
- Python 3.10+
- Docker
- Active graphical desktop session

---

## Project Structure

SDV__GUI_final/
- main.py
- ui.py
- vehicle_data.py
- Own_GUI_vss.json
- icons

---

## Full Setup (Copy & Paste One Command at a Time)

### System update
```bash
sudo apt update && sudo apt upgrade -y
```

### Install Docker
```bash
curl -fsSL https://get.docker.com | sudo sh
```

```bash
sudo usermod -aG docker $USER
```

```bash
sudo reboot
```

---

### Install Python and required system libraries
```bash
sudo apt install -y python3 python3-venv python3-pip 
```
```bash
sudo apt install -y \
libgl1 \
libegl1 \
libxkbcommon-x11-0 \
libxcb-cursor0 \
libxcb-xinerama0 \
libxcb-icccm4 \
libxcb-image0 \
libxcb-keysyms1 \
libxcb-render-util0 \
libxcb-shape0 \
libxcb-sync1 \
libxcb-xfixes0
```
---

### Clone repository
```bash
git clone https://github.com/jonahirsch/SDV__GUI_final.git && cd SDV__GUI_final
```

---

### Create Python virtual environment and install dependencies
```bash
python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install PySide6 kuksa-client
```

---

## KUKSA Databroker Setup

### Create Docker network
```bash
docker network create kuksa
```

### Start KUKSA Databroker
```bash
docker run -d --name Server --network kuksa -p 55555:55555 -v $(pwd)/Own_GUI_vss.json:/data/vss.json ghcr.io/eclipse-kuksa/kuksa-databroker:main --insecure --vss /data/vss.json
```

---

## Start the GUI Application
```bash
source venv/bin/activate && python3 main.py
```

If successful, the terminal prints:
```
Kuksa Databroker connected successfully
```

---

## Start KUKSA CLI (Second Terminal)

```bash
docker run -it --rm --network kuksa ghcr.io/eclipse-kuksa/kuksa-databroker-cli:main --server Server:55555
```

### Example CLI commands
```bash
publish Vehicle.Speed 89
```

```bash
get Vehicle.Body.Lights.Beam.High.IsOn
```

```bash
subscribe Vehicle.Body.Lights.Hazard.IsSignaling
```
All VSS Signals can be found in the VSS_GUI_Signals.txt attached wihtin the project.

---

## How It Works

- The GUI runs in the main Qt thread
- A background thread:
  - reads signals from the KUKSA Databroker
  - updates the GUI state
  - publishes GUI button states back to KUKSA
- All signals follow `Own_GUI_vss.json`

---

## Stop and Cleanup

### Stop Databroker
```bash
docker stop Server && docker rm Server
```

### Remove Docker network (optional)
```bash
docker network rm kuksa
```

---

## Notes

- GUI requires a local display (not SSH-only)
- Intended for simulation and development use
- Not intended for production vehicle systems

---



