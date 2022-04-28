# Taiwan-Criminal-Law-Interactive-Chatbot
This project is made by WIDM Lab (Web Intelligence and Data Mining Laboratory) undergraduate students of CSIE dep. (Computer Science and Inforation Engineering department) of NCU (National Central University).

## Before running
### Download data, model and checkpoint
Due to the size of data, model and checkpoint files are too large, you need to download those files and put them into the correct paths, and the program can execute correctly.
- [data](https://drive.google.com/drive/folders/1HY0_Zdik-cggjVFoG5K9ts7KmC-7-dfw?usp=sharing): put all files into `./legal_judgment_prediction/data`
- [pytorch_model.bin](https://drive.google.com/file/d/1jkSh7_UOzY637J1VMWC8uGoWCBf_uoVK/view?usp=sharing): put file into `./legal_judgment_prediction/bert/`
- [checkpoint_2.pkl](https://drive.google.com/file/d/1bzBt_8XDbS389g5_xF0uoohaofKVt9YL/view?usp=sharing): put file into `./legal_judgment_prediction/results/Bert`

### Install the modules
Run `pip install -r requirements.txt` to install all needed modules.

## How to run LJP model
This program has three mode: train, eval, serve.

All execution messages are saved in `legal_judgment_prediction/log/Bert.log`.

### Usage
```
python main.py --config [config_file_path] --gpu [gpu IDs] --mode [mode] [--checkpoint] [checkpoint_file_path] [--do_test] [--open_server]
```

### Detail of parameters
- --config, -c [config_file_path]: The path of config file. You can use default config `./config.ini`
- --gpu, -g [gpu_IDs]: The list of gpu ID. You can find gpu IDs with command `nvidia-smi -L`
- --mode, -m [mode]: There are three mode: train, eval or serve.
- --checkpoint: The path of checkpoint. (eval, serve mode required)
- --do_test: If you want to do test when training, add this parameter into instruction.
- --open_server: If you want to run this service on Line-Bot, Add this parameter into instruction.

### Train
#### Basic usage
```
python main.py --config [config_file_path] --gpu [gpu_IDs] --mode train [--checkpoint] [checkpoint_file_path] [--do_test]
```

In this mode, program will train new checkpoints.

If you add `--checkpoint [checkpoint_file_path]` into instruction, program will train new checkpoints based [checkpoint_file_path].

If you want to do test when training, add `--do_test` into instruction.

### Eval
#### Basic usage
```
python main.py --config [config_file_path] --gpu [gpu_IDs] --mode eval --checkpoint [checkpoint_file_path]
```

In this mode, program will evalute test data.

### Serve
#### Basic usage
```
python main.py --config [config_file_path] --gpu [gpu_IDs] --mode serve --checkpoint [checkpoint_file_path] [--open_server]
```

In this mode, program can predict the accuse, article and article_source of inputting string.

If you add `--open_server` into instruction, program will open Flask web server. You can use this mode with Line-Bot.

## How to run Line-Bot  
1. Move to root directory `Taiwan-Criminal-Law-Interactive-Chatbot`
2. Revise below settings in ./config.ini
    - [server]
      - server_socket_IP: This can be found with command `ifconfig`.
      - LINE_CHANNEL_ACCESS_TOKEN: This can be found in your channel on LINE Developers.
      - CHANNEL_SECRET: This can be found in your channel on LINE Developers.
3. Run ngrok with instruction `ngrok http 5000`
4. Edit `Webhook URL` in your channel on LINE Developers with the link generated by ngrok
5. Run `main.py` with `serve` mode and add `--open_server` parameter into instruction

## Demo
### Serve (simple_IO)
![Demo_simple_IO](https://i.imgur.com/dqpDRgG.png)

### Serve (open_server)
![Demo_Line](https://i.imgur.com/TSQGmtH.png)