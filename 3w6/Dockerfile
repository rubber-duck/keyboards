# Use qmkfm/qmk_cli as the base image
FROM qmkfm/qmk_cli

# Set the working directory
WORKDIR /qmk_firmware

# Clone the QMK firmware repository with submodules
RUN git clone --recurse-submodules https://github.com/qmk/qmk_firmware.git .

# QMK setup
RUN qmk setup -y
