# DOH Data Drop Django and Telegram Client

## Running the Django Server

1. First install the virtual environment in the root directory of the project with the following code:

    `python -m venv env`
2. Next we will need to activate the virtual environment. Run the Activate script from using Windows with the following code:

    `& env\Scripts\Activate.ps1`

    **NOTE:** This refers to the Windows version which was used to run this. Since this runs on the Windows version of **ngorok** (more on this later), it is suggested to use Windows in testing out this web app.
3. We will need to install the following Python packages using pip on the virtual environment:

    ```bash
    pip install django
    pip install djangorestframework
    pip install pandas
    ```

4. We will need to make and create migrations. This is in case the SQLite Database doeesn't properly set up on your machine. Navigate to the **dohdatadrop** subfolder and run the following:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Finally, run the server within the **dohdatadrop** folder by running the following and verifying it is installed:

    ```bash
    python manage.py runserver
    ```

6. Go to the default site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You should be able to register for an account and use the site.

### Using the DOH Data Drop Web App

The default landing page is the audit view that displays the username, file name, file size, and row count of uploaded files. You can click on the Upload a new file link at the top view to upload a new CSV file.

You may use the **sample.csv** file provided for in uploading data found in the root directory for a sample of 100 entries.

**NOTE:** While the site allows the upload of a single CSV file multiple times for the purposes of illustration, it will **NOT** enter duplicate data into the database thus preserving its integrity.

### DOH Data Drop API Endpoints

You can access the following api endpoints through the following links:

`http://127.0.0.1:8000/case/<case_code>`
> This will return all the details of the corresponding case code

`http://127.0.0.1:8000/total/<year>/<month>/<day>/<age>`
> This will return the number of cases which are recovered, died, and ongoing for the specified date and age. Cases that do not have a recovery date are considered as ongoing.

`http://127.0.0.1:8000/list/<year>/<month>/<day>/<age>`
> This will list down all the cases and their status being ongoing, recovered, or died for the specified date and age. Cases that do not have a recovery date are considered as ongoing.
---

## Telegram Bot

In order to use the Telegram Bot with our server running on the localhost, we will first have to use a third party tool called **ngorok** that reroutes localhost requests to the web. We will then be routing the forwarding address of **ngorok** to our Telegram Bot in order for it to work. To run the Telegram Bot, you should do the following:

1. First unblock the ngorok file. You can do this by right clicking on **ngorok.exe**, go to properties, then tick the unblock checkbox.
2. To run our server that will communicate with **ngorok**, we will need to create a light server using bottle. To do that, run the following on the virtual environment:

    ```bash
    pip install bottle requests
    ```

3. Start the server. To do this, go to the Telegram Bot directory using the terminal, and run it with the following:

    ```bash
    python bot.py
    ```

    Doing so should be able to run the server we will be using for our Telegram Bot.

4. Open a new terminal window in the same Telegram Bot folder, and run the following code:

    ```bash
    ./ngork http 8080
    ```

    You should see something similar to the screenshot below:

    ![ngorok screenshot](https://drive.google.com/uc?export=view&id=1meOTefsjm3ayMXLpnTdu6Lm4w-KflL7Z)
    **NOTE:** If the image does not display, just refresh the page or access it from [here](https://drive.google.com/file/d/1meOTefsjm3ayMXLpnTdu6Lm4w-KflL7Z/view?usp=sharing).

    As mentioned, this will allow us to forward http requests through the localhost. You can see the sample forwarding address in the screenshot above.
    As stated earlier, this will allow us to forward http requests via localhost
5. We need to then setup the custom webhook. To set this up, take note of the ngorok forwarding url in the previous step, and use the link below while replacing the ngorok url portion with the one ngorok provided you just now into your web browser:

    ```bash
    api.telegram.org/bot2103396271:AAF-pgJgQxKzn4UtJHLsDWvxZX1j1d4q6XQ/setWebHook?url=https://<insert ngorok url>
    ```

    If you do this correctly, the web browser should return the following message:

    ```json
    {"ok":true,"result":true,"description":"Webhook was set"}
    ```

6. You can then verify if the webhook connection is active through the following link through your web browser:

    ```bash
    https://api.telegram.org/bot2103396271:AAF-pgJgQxKzn4UtJHLsDWvxZX1j1d4q6XQ/getWebhookInfo
    ```

    **NOTE:** Give about 5 minutes before doing the next step, as in my experience it takes a while for the web routing to take effect in my environment.
7. Access the Telegram Bot by searching for **VictorCovidTestBot**. You can type in the commands specified and the bot should return the corresponding data.

    **NOTE: The following have to be running for the web app to work:**
    * The Django server has to be running
    * The bottle server has to be running
    * The Ngorok server has to be running

### Using the Telegram Bot

You can use the following commands for the telegram bot:

`case_search: <casenumber>`

> This will give the details of a case number. If there is none found, it will mention that none was found

`total <month/day/year> <age>`

> This will give the total number of recoveries, died, and ongoing cases for that date and age. Entries that do not have a recovery date will still be considered as ongoing.

`list <month/day/year> <age>`

> This will list all the ongoing, died, and recovered cases for the specified date and age. Entries that do not have a recovery date will still be considered as ongoing.
