def pass_function(*args, **kwargs):
    pass


def print_on_enter(vertex, predc=''):
    print('Entered {0} from {1}'.format(vertex, predc))


def print_on_exit(vertex, predc=''):
    print('Left {0} up to {1}'.format(vertex, predc))
