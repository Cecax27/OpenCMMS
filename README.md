# OpenCMMS
**OpenCMMS** is a open source project of *Computarized Maintenance Management System*. It works over Python and TKinter, and uses SQLite to manage all the data.

![Light](https://user-images.githubusercontent.com/82971436/226115629-b9d6d867-98dc-4752-978b-79046e2c17b2.jpg)

![Dark](https://user-images.githubusercontent.com/82971436/226115626-4b7b5a45-6fa8-4835-ae62-da22e666c921.jpg)

OpenCMMS is available only in spanish. If you want to colaborate to translate the software to other language, you can contact me.

## What you can do with OpenCMMS?

Right now, you can manage your preventive and corrective maintenances, your inventory, requisitions and your employers.

OpenCMMS have tools to create and export (.pdf) workordes, requisitions, and inventory.

You can have a history of your maintenances, schedule new activities and order your factory in departments, areas and plants.

## How to install?

First, you need to install Python.  You can download and install it in the oficial web: https://www.python.org/downloads/

I recommend you to download OpenCMMS with git, so go to the official web and get it:  https://git-scm.com/downloads

Once you have git and Python, open your git bash and write: 
` git clone https://github.com/Cecax27/OpenCMMS.git
`

Next, you also need to install some Python modules, in the git bash paste the next lines:

    pip install customtkinter
    pip install pandas
    pip install seaborn
    pip install reportlab
    pip install tkcalendar

### How to run?
Now you can start the app. You can launch OpenCMMS from the git bash writing:
`python main.py` or making double clic on the file "main.py".
