from echarts_data import create_app
from echarts_data.extensions import manager
from echarts_data.models.echarts_mod import *


app = create_app('development')


@manager.command
def run():
    app.run('0.0.0.0', 7000, debug=True)


if __name__ == '__main__':
    manager.run()
