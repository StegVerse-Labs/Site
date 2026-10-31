python -m unittest -v tests.test_stegos_resident_health
node --test tests/stegos-node-capabilities.test.cjs
python -m unittest discover -s tests -p test_verify_stegos_node_capabilities.py -v
