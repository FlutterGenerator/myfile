#!/bin/bash 
# Define colors
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[3;33m'
SYELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
RESET='\033[0m' # No color / Reset

# Example with background colors
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'
BG_BLUE='\033[44m'
BG_MAGENTA='\033[45m'
BG_CYAN='\033[46m'
BG_WHITE='\033[47m'


success_msg() {
echo -e " ${GREEN}[+] Successfully ✓${RESET}"
sleep 5
main
}

err_msg() {
echo -e " ${RED}[!] Something went wrong ❌${RESET}"
sleep 5
main
}

inv_msg() {
echo -e " ${RED}[!] Invalid option${RESET}"
sleep 5
}

##########################################
#                                        #
#             VIDEO TOOLS                #
#                                        #
##########################################

# Function to convert video format
convert_video_format() {
    read -p " Enter input file name (with extension): " input_file
    read -p " Enter output file name (with new extension): " output_file
    ffmpeg -i "$input_file" "${ff_folder}/$output_file" && success_msg || err_msg
sleep 5
}

# Function to extract audio from video
extract_audio() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter output audio file name (with extension, e.g., .mp3, .wav): " output_file
    ffmpeg -i "$input_file" -q:a 0 -map a "${ff_folder}/$output_file" && success_msg || err_msg
}

# Function to resize video
resize_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter output video file name (with extension): " output_file
    read -p " Enter desired resolution (e.g., 1280x720): " resolution
    ffmpeg -i "$input_file" -vf scale="$resolution" "${ff_folder}/$output_file" && success_msg || err_msg
}

# Function to trim video
trim_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter output video file name (with extension): " output_file
    read -p " Enter start time (in seconds or hh:mm:ss): " start_time
    read -p " Enter duration (in seconds or hh:mm:ss): " duration
    ffmpeg -i "$input_file" -ss "$start_time" -t "$duration" -c copy "${ff_folder}/$output_file" && success_msg || err_msg
}

# Function to add watermark to video
add_watermark() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter watermark image file name (with extension): " watermark_file
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -i "$watermark_file" -filter_complex "overlay=10:10" "${ff_folder}/$output_file" && success_msg || err_msg
}

# Function to change video speed
change_video_speed() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter output video file name (with extension): " output_file
    read -p " Enter speed factor (e.g., 0.5 for half speed, 2 for double speed): " speed_factor
    ffmpeg -i "$input_file" -filter:v "setpts=$speed_factor*PTS" "${ff_folder}/$output_file" && success_msg || err_msg
}

# Make silent video 
mute_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -an -c:v copy "${ff_folder}/$output_file" && success_msg || err_msg
}

# Extract frame
extract_frame() {
    read -p " Enter input video file name (with extension): " input_file
    ffmpeg -i "$input_file" -vf fps=1 "${ff_folder}/frames/frame_%04d.png" && success_msg || err_msg
}

# Change bitrate
change_bitrate() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter bitrate (e.g., 1000k): " bitrate
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -b:v "$bitrate" "${ff_folder}/$output_file" && success_msg || err_msg
}

# Add audio to silent video
add_audio_to_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter input audio file name (with extension): " input_audio
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -i "$input_audio" -c:v copy -c:a aac -strict experimental "${ff_folder}/$output_file" && success_msg || err_msg
}

# Replace audio in video
replace_audio_in_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter input audio file name (with extension): " input_audio
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -i "$input_audio" -map 0:v -map 1:a -c:v copy -c:a aac -strict experimental "${ff_folder}/$output_file" && success_msg || err_msg
}

# Add text
overlay_text_on_video() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter your text for overlay: " text
    read -p " Enter font color (e.g., white): " fn_color
    read -p " Enter font size (e.g., 24): " fn_size
    read -p " Enter x position (e.g., 10): " x
    read -p " Enter y position (e.g., 10): " y
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -vf "drawtext=text='"$text"':fontcolor=$fn_color:fontsize=$fn_size:x=$x:y=$y" -codec:a copy "${ff_folder}/$output_file" && success_msg || err_msg
}

# Add metadata 
add_metadata() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter author name: " author
    read -p " Enter title name: " title
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -i "$input_file" -metadata title="$title" -metadata author="$author" "${ff_folder}/$output_file" && success_msg || err_msg
}

#Extract Video Segment
extract_segment() {
    read -p " Enter input video file name (with extension):" input_file
    read -p " Enter start time (in seconds or hh:mm:ss): " start_time
    read -p " Enter duration (in seconds or hh:mm:ss): " duration
    read -p " Enter output video file name (with extension):" output_file
    ffmpeg -i "$input_file" -ss "$start_time" -t "$duration" -c copy "${ff_folder}/$output_file" && success_msg || err_msg
}

#Apply Video Filters
apply_filter() {
    read -p " Enter input video file name (with extension):" input_file
    echo -e " [1] Grayscale\n [2] Blur"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read filter
    read -p " Enter output video file name (with extension):" output_file

if [[ $filter -eq 1 ]]; then
ffmpeg -i "$input_file" -vf "hue=s=0" "${ff_folder}/$output_file" && success_msg || err_msg
elif [[ $filter -eq 2 ]]; then
ffmpeg -i "$input_file" -vf "boxblur=10:1" "${ff_folder}/$output_file" && success_msg || err_msg
else 
inv_msg
fi
}

compress_video() {
read -p " Enter input video file name (with extension):" input_file
echo -e " ${GREEN}[1] very-high${RESET}"
echo -e "\e[33m [2] high\e[0m";
echo -e " ${BLUE}[3] medium${RESET}";
echo -e "\e[35m [4] low\e[0m";
echo -e " ${RED}[5] very-low${RESET}";
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
read -p " Enter output video file name (with extension):" output_file

if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -c:v libx264 -crf 25 -preset veryfast "${ff_folder}/very_high_$output_file" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -c:v libx264 -crf 28 -preset veryfast "${ff_folder}/high_$output_file" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -c:v libx264 -crf 30 -preset veryfast "${ff_folder}/medium_$output_file" && success_msg || err_msg
elif [[ $option -eq 4 ]]; then
ffmpeg -i "$input_file" -c:v libx264 -crf 32 -preset veryfast "${ff_folder}/low_$output_file" && success_msg || err_msg
elif [[ $option -eq 5 ]]; then
ffmpeg -i "$input_file" -c:v libx264 -crf 35 -preset veryfast "${ff_folder}/very_low_$output_file" && success_msg || err_msg
else
inv_msg
fi
}
create_cfg() {
input=""
output_file="/sdcard/input.txt"
while true; do
echo -en " Write file's path: "; read input
echo -en " Stop conversation[y/n]? "; read yesno
if [[ "$yesno" == "y" ]]; then
break
else
input0+="
file '$input'"
cat > ${output_file} << EOF
${input0}
EOF
fi
done
merge_videos
}

merge_videos() {
if [[ -f "/sdcard/input.txt" ]]; then
    read -p " Enter output video file name (with extension): " output_file
    ffmpeg -f concat -safe 0 -i "/sdcard/input.txt" -c copy "${ff_folder}/$output_file"; rm -f '/storage/emulated/0/input.txt' && success_msg || err_msg
else
create_cfg
fi
}

##########################################
#                                        #
#              AUDIO TOOLS               #
#                                        #
##########################################

main_audio() {
read -p " Enter input file name (with extension): " input_file
echo -e " ${MAGENTA}[Filters]\n [1] Remove vocal\n [2] Nightcore\n [3] 8d\n [4] Vaporwave\n [5] Boost bass\n [6] Chorus\n [7] High-pass Filter For a Vintage Feel\n [8] Reverb\n [9] Indoor\n [10] Treble boost\n [11] Pitch shift\n [12] Tempo change\n [13] Flanger\n [14] Lo-Fi\n [15] Echo${RESET}\n ${SYELLOW}[b] Back to main${RESET}\n ${RED}[e] Exit${RESET}"
echo -en " ${YELLOW}[>] Choose an option:${RESET} "; read filter_audio
case $filter_audio in
    "e") exit ;;
    "b") main ;;
esac
if [[ $filter_audio -eq 1 ]]; then     # Remove vocal
echo -e " [1] Stable\n [2] Beta"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -af "stereotools=mlev=0.03" "${ff_folder}/output.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -af "pan=stereo|c0=c0|c1=-1*c1" "${ff_folder}/output.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 2 ]]; then # Nightcore
echo -e " ${MAGENTA}[1] 30% (standard)\n [2] 20%\n [3] 25%${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*1.3,atempo=1/1.3,aresample=44100" "${ff_folder}/output_nightcore.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*1.2,atempo=1/1.2,aresample=44100" "${ff_folder}/output_nightcore_20.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*1.25,atempo=1/1.25,aresample=44100" "${ff_folder}/output_nightcore_25.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 3 ]]; then #8d
echo -e " ${MAGENTA}[1] Standard\n [2] Slower\n [3] Faster${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -filter_complex "apulsator=hz=0.08" "${ff_folder}/output_8d.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -filter_complex "apulsator=hz=0.05" "${ff_folder}/output_8d_slow.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -filter_complex "apulsator=hz=0.15" "${ff_folder}/output_8d_fast.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 4 ]]; then #Vaporwave
echo -e " ${MAGENTA}[1] 30%(standard)\n [2] 20%\n [3] 25%${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*0.7,atempo=1.0,aresample=44100" "${ff_folder}/output_vaporwave.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*0.8,atempo=1.0,aresample=44100" "${ff_folder}/output_vaporwave_20.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -filter_complex "asetrate=44100*0.75,atempo=1.0,aresample=44100" "${ff_folder}/output_vaporwave_25.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 5 ]]; then #Boost bass

echo -e " ${MAGENTA}[1] 10dB(standard)\n [2] 15dB(high)\n [3] 6dB(moderate)${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -af "equalizer=f=50:width_type=h:width=200:g=10" "${ff_folder}/output_bass_boost.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -af "equalizer=f=50:width_type=h:width=200:g=15" "${ff_folder}/output_bass_boost_high.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -af "equalizer=f=50:width_type=h:width=200:g=6" "${ff_folder}/output_bass_boost_moderate.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 6 ]]; then #Chorus
ffmpeg -i "$input_file" -af "chorus=0.6:0.9:55:0.4:0.25:2" "${ff_folder}/output_chorus.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 7 ]]; then #High-pass Filter For a Vintage Feel
ffmpeg -i "$input_file" -af "highpass=f=300,lowpass=f=3000" "${ff_folder}/output_vintage.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 8 ]]; then #Reverb
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:1000:0.3" "${ff_folder}/output_reverb.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 9 ]]; then #Indoor
echo -e " ${MAGENTA}[1] Standard\n [2] Advanced\n [3] Shorter\n [4] Longer${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.88:60:0.4" "${ff_folder}/output_indoor.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -af "afftdn, aecho=0.8:0.88:1000:0.3" "${ff_folder}/output_indoor_afftdn.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:50:0.5" "${ff_folder}/output_indoor_shorter.mp3" && success_msg || err_msg
elif [[ $option -eq 4 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:100:0.7" "${ff_folder}/output_indoor_longer.mp3" && success_msg || err_msg
else
inv_msg
fi
elif [[ $filter_audio -eq 10 ]]; then #Treble boost
ffmpeg -i "$input_file" -af "treble=g=10" "${ff_folder}/output_treble_boost.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 11 ]]; then #Pitch shift
ffmpeg -i "$input_file" -af "asetrate=44100*1.2,aresample=44100" "${ff_folder}/output_pitch_shift.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 12 ]]; then #Tempo change
read -p " Change temp of audio (must be between 0.5 and 2.0): " atempo
ffmpeg -i "$input_file" -af "atempo=$atempo" "${ff_folder}/output_tempo_change.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 13 ]]; then #Flanger
ffmpeg -i "$input_file" -af "flanger" "${ff_folder}/output_flanger.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 14 ]]; then #Lo-Fi
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:1000:0.3" "${ff_folder}/output_lofi.mp3" && success_msg || err_msg
elif [[ $filter_audio -eq 15 ]]; then #Echo
echo -e " ${MAGENTA}[1] Simple\n [2] Multiple echoes\n [3] Short delay high decay${RESET}"
echo -en " ${YELLOW}[>] Choose an option: ${RESET}"; read option
if [[ $option -eq 1 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:1000:0.3" "${ff_folder}/output_echo.mp3" && success_msg || err_msg
elif [[ $option -eq 2 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:500|1000:0.2|0.3" "${ff_folder}/output_with_multiple_echoes.mp3" && success_msg || err_msg
elif [[ $option -eq 3 ]]; then
ffmpeg -i "$input_file" -af "aecho=0.8:0.9:250:0.6" "${ff_folder}/short_delay_high_decay.mp3" && success_msg || err_msg
else 
inv_msg
fi
fi

}
#Normalize Audio Volume
fix_audio() {
    read -p " Enter input video or audio file name (with extension):" input_file
    read -p " Enter output file name (with extension):" output_file
    ffmpeg -i "$input_file" -af "volume=1.5" "${ff_folder}/$output_file" && success_msg || err_msg
}

equalizer() {
# f=1000 sets the center frequency to 1000 
# Hz.t=q sets the filter type to quality factor.
# w=1 sets the width of the frequency band.
# g=5 sets the gain to 5 dB.
read -p " Enter input audio file name (with extension):" input_file
read -p " Enter the center frequency (eg., 1000): " freq
read -p " Enter the filter type (eg., q): " flt_type
read -p " Enter the width of the frequency band (eg., 1): " w_freq
read -p " Enter the gain (dB) (eg., 5): " gain
read -p " Enter output audio file name (with extension):" output_file
ffmpeg -i input.mp3 -af "equalizer=f=$freq:t=$flt_type:w=$w_freq:g=$gain" "${ff_folder}/output-equalized.mp3" && success_msg || err_msg
}

trim_audio() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter start time (in seconds or hh:mm:ss): " start_time
    read -p " Enter duration (in seconds or hh:mm:ss): " duration
    read -p " Enter output audio file name (with extension): " output_file
ffmpeg -i "$input_file" -ss "$start_time" -to "$duration" -c copy "${ff_folder}/$output_file" && success_msg || err_msg
}

add_meta() {
    read -p " Enter input video file name (with extension): " input_file
    read -p " Enter title name: " title
    read -p " Enter artist name: " artist
    read -p " Enter output audio file name (with extension): " output_file
   ffmpeg -i "$input_file" -metadata title="$title" -metadata artist="$artist" "${ff_folder}/$output_file"  && success_msg || err_msg
}

compress_audio() {
read -p " Enter input video file name (with extension): " input_file
echo -en " Select bitrate(${MAGENTA}32, ${MAGENTA}64, ${MAGENTA}96${RESET}, ${MAGENTA}112${RESET}, ${MAGENTA}128${RESET}, ${MAGENTA}160${RESET}, ${MAGENTA}192${RESET}, ${MAGENTA}256${RESET}, ${MAGENTA}320${RESET}): "; read bitrate
read -p " Enter output audio file name (with extension): " output_file
ffmpeg -i "$input_file" -ab $bitrate "${ff_folder}/$output"  && success_msg || err_msg
}

credits() {
echo -e "${CYAN} Main Author: toyly_s${RESET}"
sleep 2
echo -e "${GREEN} Script version: 2.0${RESET}"
sleep 2
echo -e "${YELLOW} More futures will be added soon...${RESET}"
sleep 8
}

# Main menu
main() {
ff_folder='/storage/emulated/0/ffmpeg'
while true; do
clear
echo -e "               ${GREEN}____________${RESET}\n              ${GREEN}/ ____/ ____/${RESET}${WHITE}___ ___  ____  ___  ____ _${RESET}\n             ${GREEN}/ /_  / /_${RESET}  ${WHITE}/ __ \`__ \/ __ \/ _ \/ __ \`/${RESET}\n            ${GREEN}/ __/ / __/${RESET} ${WHITE}/ / / / / / /_/ /  __/ /_/ /${RESET}\n           ${GREEN}/_/   /_/${RESET}   ${WHITE}/_/ /_/ /_/ .___/\___/\__, /${RESET}\n                                ${WHITE}/_/${RESET}         ${WHITE}/____/${RESET}"
    echo -e  "   ${BLUE}[Video tools]${RESET}                              ${MAGENTA}[Audio tools]${RESET}"
    echo -e  " ${BLUE}[1] Video converter${RESET}                      ${MAGENTA}[18] Apply filter${RESET}"
    echo -e  " ${BLUE}[2] Extract audio from video${RESET}             ${MAGENTA}[19] Fix audio${RESET}"
    echo -e  " ${BLUE}[3] Resize video${RESET}                         ${MAGENTA}[20] Equalizer(beta)${RESET}"
    echo -e  " ${BLUE}[4] Trim video${RESET}                           ${MAGENTA}[21] Trim audio${RESET}"
    echo -e  " ${BLUE}[5] Add watermark to video${RESET}               ${MAGENTA}[22] Add meta-data${RESET}"
    echo -e  " ${BLUE}[6] Change video speed${RESET}                   ${MAGENTA}[23] Compress audio${RESET}"
    echo -e  " ${BLUE}[7] Mute video${RESET}                           ${MAGENTA}[24] Coming soon${RESET}"
    echo -e  " ${BLUE}[8] Extract frame${RESET}                        ${MAGENTA}[25] Coming soon${RESET}"
    echo -e  " ${BLUE}[9] Change bitrate${RESET}                       ${MAGENTA}[26] Coming soon${RESET}"
    echo -e  " ${BLUE}[10] Add audio to silent video${RESET}           ${MAGENTA}[27] Coming soon${RESET}"
    echo -e  " ${BLUE}[11] Replace audio in video${RESET}              ${MAGENTA}[28] Coming soon${RESET}"
    echo -e  " ${BLUE}[12] Add meta-data${RESET}                       ${MAGENTA}[29] Coming soon${RESET}"
    echo -e  " ${BLUE}[13] Add overlay text${RESET}                    ${MAGENTA}[30] Coming soon${RESET}"
    echo -e  " ${BLUE}[14] Extract segment${RESET}                     ${MAGENTA}[31] Coming soon${RESET}"
    echo -e  " ${BLUE}[15] Apply filter${RESET}                        ${MAGENTA}[32] Coming soon${RESET}"
    echo -e  " ${BLUE}[16] Compress video${RESET}                      ${MAGENTA}[33] Coming soon${RESET}"
    echo -e  " ${BLUE}[17] Merge videos${RESET}"
    echo -e  " ${CYAN}[c] Credits/Info${RESET}"
    echo -e  " ${RED}[e] Exit${RESET}"
 rm -f '/storage/emulated/0/inputX.txt'
echo -en " ${YELLOW}[>] Choose an option:${RESET} "; read choice
    case $choice in
        1) convert_video_format ;;
        2) extract_audio ;;
        3) resize_video ;;
        4) trim_video ;;
        5) add_watermark ;;
        6) change_video_speed ;;
        7) mute_video ;;
        8) extract_frame ;;
        9) change_bitrate ;;
        10) add_audio_to_video ;;
        11) replace_audio_in_video ;;
        12) add_metadata ;;
        13) overlay_text_on_video ;;
        14) extract_segment ;;
        15) apply_filter ;;
        16) compress_video ;;
        17) merge_videos ;;
        18) main_audio ;;
        19) fix_audio ;;
        20) equalizer ;;
        21) trim_audio ;;
        22) add_meta ;;
        23) compress_audio ;;
        "e") exit ;;
        "c") credits ;;
        *) inv_msg ;;
    esac
done

}
main