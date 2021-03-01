

# sudo sh -c "echo 0 > /sys/bus/usb/devices/1-3/authorized"
# sudo sh -c "echo 1 > /sys/bus/usb/devices/1-3/authorized"
# sudo sh -c "echo 0 > /sys/bus/usb/devices/2-1.4/authorized"
# sudo sh -c "echo 1 > /sys/bus/usb/devices/2-1.4/authorized"

reset_usb(){
    sudo sh -c "echo 0 > $1/authorized"
    sudo sh -c "echo 1 > $1/authorized"
}

for X in /sys/bus/usb/devices/*; do
    if [ -f "$X/idVendor" ]; then
        vendor=`cat "$X/idVendor"`
        if [ $vendor == "8086" ] || [ $vendor == "8087" ]; then
            echo "resetting `lsusb -d $vendor:`"
            reset_usb $X
        fi
    fi
    # cat "$X/idVendor" 2>/dev/null
    # cat "$X/idProduct" 2>/dev/null
    # echo
done

for i in /sys/bus/pci/drivers/[uoex]hci_hcd/*:*; do
  [ -e "$i" ] || continue
  echo "${i##*/}" > "${i%/*}/unbind"
  echo "${i##*/}" > "${i%/*}/bind"
done


# lsusb -d 8086:
# lsusb -d 8087:
