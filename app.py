from flask import Flask, jsonify, request, render_template
from simulation import EpidemicSimulation
from util import default_app_input
from util import field_metadata
from util import Keys


app = Flask(__name__)


def get_simulation_inputs(configs):
    result = { 'network_config': { Keys.NETWORK_TYPE: 'ER' }, 'virus_config': {} }
    for key, val in configs.items():
        config_type, config_key = key.split('.')
        try:
            result[config_type][config_key] = int(val)
        except:
            try:
                result[config_type][config_key] = float(val)
            except:
                result[config_type][config_key] = val
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        output = {
            Keys.OUTPUT_IMAGE_URL: 'static/graphs/baseline.png',
            Keys.EPIDEMIC_DURATION: 54,
            Keys.PEAK_CASES: 2042
        }
        return render_template('index.html', input=default_app_input, output=output, field_metadata=field_metadata)
    else:
        try:
            simulation_inputs = get_simulation_inputs(request.form)
            simulation = EpidemicSimulation(**simulation_inputs, seed=10)
            return render_template('index.html', input=request.form, output=simulation.simulate(), field_metadata=field_metadata)
        except:
            resp = jsonify({'message': "Something's not quiet right..."})
            resp.status_code = 400
            return resp

if __name__ == '__main__':
    app.run(debug=True)
