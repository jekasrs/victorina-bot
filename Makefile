deps:
	python -m pip install pyTelegramBotAPI telebotapi TelegramBotAPI pyrogram asyncio tgintegration

pull:
	git pull

test: # Unit test
	python -m testSession

run:
	python main.py &

test: # Integration test
	python -m integrationTest

clean:
	rm -r __pycache__
	rm my_account.session