# DatabaseServer

Database server of AwesomeTickets system.

## Installation

- Requirements

    - MySQL 5.7
    - username: root
    - password: 123456

- Initialize data

    ```bash
    $ pip3 install -r requirements.txt
    $ python3 init.py
    ```

- Run with docker

    ```bash
    $ docker build -t db-server .
    $ docker run --name db-server -p 3306:3306 -d db-server
    ```

## Models

### Conceptual data model

![](https://raw.githubusercontent.com/AwesomeTickets/Database/master/img/model/conceptual_data_model.png)

### Physical data model

![](https://raw.githubusercontent.com/AwesomeTickets/Database/master/img/model/physical_data_model.png)

## Credits

- PowerDesigner 16.5.0

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.
