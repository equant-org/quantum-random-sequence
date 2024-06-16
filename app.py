from flask import Flask, request, jsonify
from qiskit import QuantumCircuit, Aer, execute

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate_random_sequence():
	length = int(request.args.get('length', 1))
	
	# Create a Quantum Circuit with 'length' qubits and classical bits
	qc = QuantumCircuit(length, length)
	qc.h(range(length))  # Apply Hadamard gate to put all qubits in superposition
	qc.measure(range(length), range(length))  # Measure all qubits
	
	# Use the Aer's qasm_simulator
	simulator = Aer.get_backend('qasm_simulator')
	
	# Execute the circuit on the qasm simulator
	job = execute(qc, simulator, shots=1)
	
	# Grab results from the job
	result = job.result()
	counts = result.get_counts(qc)
	
	# The result will be a dictionary with a binary string as the key
	random_sequence = list(counts.keys())[0]
	
	return jsonify(random_sequence=random_sequence)

if __name__ == '__main__':
	app.run(debug=True)
