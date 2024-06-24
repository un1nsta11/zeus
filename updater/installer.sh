#!/usr/bin/env sh
# ----------------------------------------------------------------------------------------------------------------------
# Title: Zeus Installer
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------
log_info() {
  echo $(date) "[INFO ] $1"
}
log_error() {
  echo $(date) "[ERROR] $1"
}
log_warn() {
  echo $(date) "[WARN ] $1"
}

# ----------------------------------------------------------------------------------------------------------------------
# Variables
# ----------------------------------------------------------------------------------------------------------------------
installer_path="/zeus"
updater_path="/zeus/updater"
local_repository="/zeus/zeus"

# ----------------------------------------------------------------------------------------------------------------------
# Main Functions
# ----------------------------------------------------------------------------------------------------------------------
cleanup() {
  log_info "Cleanup: remove any application directories if they are exist"
  if [ -d $installer_path ]; then
    rm -r $installer_path
  fi
}

make_dirs() {
  log_info "Create application directories"
  mkdir $installer_path
  mkdir $updater_path
}

clone() {
  log_info "Clone repository to the application directory"
  git clone $local_repository $installer_path
}

dependencies() {
  log_info "Install required dependencies"
  python3 -m pip install pyTelegramBotAPI
}

launcher() {
  log_info "Copy launcher into updater and make it executable"
  cp $local_repository/updater/zeus-launcher.sh $updater_path/zues-launcher.sh
  chmod +x $local_repository/updater/zeus-launcher.sh
  log_info "Add launcher into startup system file"
  echo  @reboot sh $local_repository/updater/zeus-launcher.sh >> /etc/crontab
  log_info "Adding zeus-launcher into startup completed with error level: $?"
}

# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------
cleanup
make_dirs
clone
launcher
exit 0

