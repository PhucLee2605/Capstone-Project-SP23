from src import create_app
import warnings
warnings.filterwarnings("ignore")

app = create_app()

app.run(debug=False, host='0.0.0.0', port=5001)
