# ambientwx-to-cwop
This software relays data from the AmbientWeather API to CWOP.  I currently run this with a Python Lambda in AWS for minimal if not zero monthly cost.

# Setup
1) Register at ambientweather: https://ambientweather.net/ and provision an API Key (Note you only need an API key, use the application key included in the code)
2) Register a CWOP station: http://wxqa.com/
3) Replace the entries at the top of the code with you specific MAC, API KEY, etc.  LATLON is a specific format needed by CWOP  Phillip Gladstone has a great tutorial (http://pond1.gladstonefamily.net:8080/aprswxnet.html)
4) Create a Lambda function (or deploy to your own server) and set on a schedule to run, I currently use and recommend every 5 minutes.
