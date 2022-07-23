Simplified version of https://github.com/wroscoe/donkey/

### Getting started. 
After building a Donkey2, here are the steps to start driving.

install donkey
```
git clone https://github.com/robocars/donkey donkeycar
pip install -e donkeycar
```

Create a car folder.
```
donkey createcar --path ~/d2
```

Start your car.
```
python ~/d2/manage.py drive
```

Now you can control your car by going to `<ip_address_of_your_pi>:8887/drive`
