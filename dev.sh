
ACTION=$1
if [ "${ACTION}" = "" ]; then
    echo "Action not provided\nSupported actions - start | stop | status | reset | scan\nEg: ./dev.sh start" >&2
    exit 1
fi

if [ "${ACTION}" = "start" ]; then
    echo "--- Starting 6 services ---------------------------"

    cd ./backend
    screen -S ai_alc_rerank -dm bash -c "source vs_env/bin/activate && python -m services.rerank"
    screen -S ai_alc_faiss -dm bash -c "source vs_env/bin/activate && python -m services.vfaiss"
    screen -S ai_alc_parse -dm bash -c "source vs_env/bin/activate && python -m services.parse"
    screen -S ai_alc_celery -dm bash -c "source vs_env/bin/activate && celery -A tasks.extract worker --loglevel=INFO -c1"

    screen -S ai_alc_api_server -dm bash -c "source vs_env/bin/activate && uvicorn services.api_server:app --reload"

    cd ../frontend
    screen -S ai_alc_ui -dm bash -c "npm start"

    cd ..

    echo "--- Services started ----------------------------"
    screen -ls
fi

if [ "${ACTION}" = "stop" ]; then
    echo "--- Stoping services ----------------------------"

    screen -S ai_alc_rerank -X quit
    screen -S ai_alc_faiss -X quit
    screen -S ai_alc_parse -X quit
    screen -S ai_alc_ui -X quit

    # Shuts down all celery
    celery control shutdown

    # Send double ctrl+C to API server screen
    screen -S ai_alc_api_server -p 0 -X stuff $'\003'
    screen -S ai_alc_api_server -p 0 -X stuff $'\003'

    screen -S ai_alc_ui -X quit

    echo "--- Stoped services -----------------------------"
    screen -ls
fi

if [ "${ACTION}" = "status" ]; then
    screen -ls
fi

if [ "${ACTION}" = "reset" ]; then
  cd ./backend
  python -m scripts.setup
  cd ..
fi

if [ "${ACTION}" = "scan" ]; then
  cd ./backend
  python -m scripts.file_scanner
  cd ..
fi
