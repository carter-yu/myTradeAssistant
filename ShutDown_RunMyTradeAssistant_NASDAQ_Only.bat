@ECHO Off

REM C:\Users\Carter\Anaconda3\python.exe C:\Users\Carter\Interactive_Brokers\myTradeAssistant\myTradeAssistant.py DAILY_PRICE NASDAQ_INFO GOOG_NEWS
REM C:\Users\Carter\Anaconda3\python.exe C:\Users\Carter\Interactive_Brokers\myTradeAssistant\myTradeAssistant.py NASDAQ_INFO 
C:\Users\Carter\Anaconda3\envs\Python_3_6\python.exe C:\Users\Carter\Interactive_Brokers\myTradeAssistant\myTradeAssistant.py NASDAQ_INFO

REM Program end. Process to shut down PC.
C:\Windows\System32\shutdown.exe /S /F /T 300

:choice
SET /P choice="Your computer is about to shutdown in 5 min do you want to abort (y/n): "
IF %choice% EQU y (
  C:\Windows\System32\shutdown.exe /A
  C:\Windows\System32\timeout.exe /T 600 /NOBREAK
  GOTO choice
) ELSE (
  ECHO Invalid Input. 'y' for abort shutdown.
  GOTO choice
)