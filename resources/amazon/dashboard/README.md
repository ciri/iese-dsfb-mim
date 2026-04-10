This is inspired by https://github.com/mayaradaher/challenge-Amazon.

Requires:

```
conda create -n dashboard python=3.11 -y
conda activate dashboard
pip install dash dash-bootstrap-components pandas
```

Then run it by doing:

```
conda activate dashboard
python app.py
```

And navigate to `http://127.0.0.1:8050/`
`
If it complains about packages not being installed you will need to install those first as well.