# Database

Data models and initialization scripts of AwesomeTickets database.

## Installation

1. Download [MySQL](https://dev.mysql.com/downloads/mysql/).

2. Create user:

    ```
    username: root
    password: 123456
    ```

3. Initialize database:

    ```sh
    $ pip3 install PyMySQL
    $ python3 init_db.py
    ```

## Conceptual data model

![](https://raw.githubusercontent.com/AwesomeTickets/Database/master/img/model/conceptual_data_model.png)

## Physical data model

![](https://raw.githubusercontent.com/AwesomeTickets/Database/master/img/model/physical_data_model.png)

## Credits

- PowerDesigner 16.5.0

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.