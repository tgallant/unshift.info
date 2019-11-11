from .example_action import ExampleAction


action_types = {
    'example_action': ExampleAction,
}


def make_action(configuration):
    action_type = configuration.get('action_type')
    print(action_type)
    action = action_types.get(action_type)
    return action(configuration)


__all__ = ['make_action']
