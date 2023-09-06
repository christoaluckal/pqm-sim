import os
urdf_loc = "/home/caluckal/Developer/f1tenth/ros1_ws/src/pqm-sim/ouster_description/urdf"
urdf_file = "OS1-128-N1.urdf.xacro"

urdf = os.path.join(urdf_loc,urdf_file)

os_name = 0
min_angle = -45
max_angle = 45

n_beams = 128

noise_profile = 1
noise_val = 0.008

base_name = f'OS1-128-N1'

full_name = f'OS{os_name}-{n_beams}-N{noise_profile}'

with open(urdf,'r') as f:
    line_list = f.readlines()

    for x in line_list:
        # print(x,f'name="{full_name}"')

        if x.find(f'name="{base_name}"') != -1:
            print(x)
            x.replace(f'"{base_name}"',f'"{full_name}"',-1)
            print(x)

            
    # for x in line_list:
    #     if x.find(f'lasers:=128') != -1:
    #         print("laser")
    #         print(x)
    #         x.replace(f'lasers:=128',f'lasers:={n_beams}')
    #         print(x)

    # for x in line_list:
    #     if x.find(f'noise:=0.008') != -1:
    #         print("noise")
    #         print(x)
    #         x.replace(f'noise:=0.008',f'noise:={noise_val}')
    #         print(x)

    # for x in line_list:
    #     if x.find(f'22.5*M_PI/180.0') != -1:
    #         print("max")
    #         print(x)
    #         x.replace(f'22.5*M_PI/180.0',f'{max_angle}*M_PI/180.0')
    #         print(x)

    # for x in line_list:
    #     if x.find(f'-22.5*M_PI/180.0') != -1:
    #         print("min")
    #         print(x)
    #         x.replace(f'-22.5*M_PI/180.0',f'{min_angle}*M_PI/180.0')
    #         print(x)

            