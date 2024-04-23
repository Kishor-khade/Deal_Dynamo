# Deal Dynamo

Deal Dynamo is a showcase application for displaying deals.

## Setup Instructions

Follow these steps to set up the application:

1. **Create API Credentials**: Use [this link](https://my.telegram.org/) to create API credentials. Make sure to note down the username, API ID, and API hash.

2. **Create Configuration File**: Create a file named `telethon.config` in the `Deal_Dynamo` folder and use the following syntax:

    ```ini
    [telethon_credentials]
    api_id = fill_up_your_api_ID 
    api_hash = use_your_api_hash 
    username = use_your_username
    ```

3. **Install Dependencies**: Run the following command to install all the dependencies:

    ```bash
    $ pip install -r requirements.txt
    ```

## Usage

Once the setup is complete, you can run the application using the following commands:

1. **Fetch Live Data**: Run the following command to fetch live data from your Telegram bot:

    ```bash
    $ python update.py
    ```

2. **Data Transformation**: Execute the following command to transform the raw data into a categorized format:

    ```bash
    $ python ML.py
    ```

3. **Run the Application**: Finally, start the application locally by running:

    ```bash
    $ python app.py
    ```

## Notes

- Make sure to replace placeholders such as `fill_up_your_api_ID` and `use_your_api_hash` with your actual API credentials.
- For more information or assistance, refer to the [Telethon documentation](https://telethon.dev/).

