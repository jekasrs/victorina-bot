#deps:
#	python -m pip install pyTelegramBotAPI telebotapi TelegramBotAPI pyrogram asyncio tgintegration
.PHONY: all run test clean 

all: run test 

run:
	python main.py &

test: # Integration test
	python -m testSession
	python -m integrationTest

clean:
	killall main.py
	rm -r __pycache__
	rm my_account.session
