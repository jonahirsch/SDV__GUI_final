# SDV_UI_Kuksa

Run Server databroker mit eigener VSS datei: 
docker run --name Server --network kuksa -p 55555:55555 -v C:\Users\jona-\OneDrive\Desktop\Business\Studium\Semester_6\Seminar\Own_GUI_vss.json:/data/vss.json ghcr.io/eclipse-kuksa/kuksa-databroker:main --insecure --vss /data/vss.json

Zweites CMD - databroker client:
docker run -it --rm --network kuksa ghcr.io/eclipse-kuksa/kuksa-databroker-cli:main --server Server:55555
