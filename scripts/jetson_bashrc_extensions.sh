#pyrealsense2
export PYTHONPATH=$PYTHONPATH:"/home/yousof/libs/librealsense_binary/python"
# pydoc -n only works for python 3.7+
# for less you should use withou -n and ip 
# and then create port forwarding with ssh to access it remotely.
alias pydocs_usb="python3 -m pydoc -n 192.168.55.1 -p 8989"
alias pydocs_wifi="python3 -m pydoc -n 192.168.0.10 -p 8989"

# port forwarding
alias pydocs_forward_port="ssh -R 8989:localhost:8989 192.168.0.7"
# or run `ssh -L 8989:localhost:8989 192.168.55.1` on host