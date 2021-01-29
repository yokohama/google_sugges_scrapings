FROM python:3

ENV APP_HOME /app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
COPY . $APP_HOME
 
RUN apt-get update && apt-get install -y unzip
 
#install google-chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

RUN apt install -y fonts-ipafont
#RUN apt-get install -y ipa-gothic-fonts ipa-mincho-fonts ipa-pgothic-fonts ipa-pmincho-fonts
 
#install selenium
RUN pip install selenium
RUN pip install gspread oauth2client
RUN pip install python-dotenv
 
#install ChromeDriver
ADD https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip
 
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

#CMD ["python", "apple.py"]
CMD ["python", "hello.py"]
