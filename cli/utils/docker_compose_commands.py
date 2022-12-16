import os


def start_docker_compose(args, command=["up", "-d"]):

    command_string = " ".join(command)
    execute_command = f"{get_docker_compose_command(args)} {command_string}"
    print(execute_command)

    return os.system(execute_command)


def get_docker_compose_command(args):
    return f"{args.docker_compose_command} -f {args.docker_compose_file}"


def stop_docker_compose(args, command=["down", "-v"]):

    command_string = " ".join(command)
    execute_command = f"{get_docker_compose_command(args)} {command_string}"
    print(execute_command)

    return os.system(execute_command)
