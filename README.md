## ScreenshotBot

Simple bot that allow you to take screenshot of site page, also you receive a status code.

### HOW TO BUILD AND RUN
```bash
docker build -t <tag> . 

# mount dir to save screenshots persistenly
docker run -v "$(pwd)/screenshots":/app/screenshots <tag> 
```
### HOW TO TEST
```bash
python3 -m unittest