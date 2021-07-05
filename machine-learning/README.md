# Setup

## Virtualenv

[Documentation](https://docs.python-guide.org/dev/virtualenvs/)

### Create virtualenv

```bash
virtualenv [name]

source [name]/bin/activate
```

### Install packages
```bash
pip install -r requirements.txt
```


# Model


## References
[Image classification](https://www.analyticsvidhya.com/blog/2020/10/create-image-classification-model-python-keras/) | [Tensorflow](https://www.tensorflow.org/tutorials/images/classification) | [Saved model](https://www.tensorflow.org/js/tutorials/conversion/import_saved_model)


## Commands

### Prepare

This command copies the images and adjustes to a workable format.
```bash
make preapre
```

### Train
This command creates the model, trains it and saves it.
```bash
make train
```

### Test
This command uses the saved model and makes predictions.
```bash
make test
```

Alternatively you could run all commands by executing:
```bash
make
```

**Note**: A copy of the images is needed, please contact me.
