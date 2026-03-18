import logging
import azure.functions as func
from fetch_data import fetch_and_process_data
from storage_helper import upload_data_to_blob

app = func.FunctionApp()

@app.timer_trigger(schedule="%Timer_Schedule%", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def energyDataTimer(myTimer: func.TimerRequest) -> None:

    try:
        if myTimer.past_due:
            logging.warning("The timer trigger is running late")   
        data = fetch_and_process_data()
        if not data:
            logging.error("No data fetched from API")
            return
        upload_data_to_blob(data)
        logging.info(data)

    except Exception as e:
        logging.error(f"execution failed : {e}")    