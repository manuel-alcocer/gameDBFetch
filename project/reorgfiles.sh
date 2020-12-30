#!/bin/bash

# Script by: Manuel Alcocer Jiménez

DATE=$(date +%F-%H%M%S)

DST_BASEDIR='/disks/crucial1TBssd/dreamcast_128/redump'
#
#
#for directory in *; do
#    if [[ -f "${directory}/name.txt" ]]; then
#        game_name="$(cat ""${directory}/name.txt"")"
#    fi
#    if [[ ! -z "${game_name}" ]] && [[ ! "$directory" == "${game_name}" ]]; then
#        echo "Moving: ${directory} -> ${game_name}" | tee -a ../chdman-${DATE}.log
#        mv -v "$directory" "${game_name}" | tee -a ../chdman-${DATE}.log
#        directory="${game_name}"
#    fi
#    unset game_name
#    if [[ -d "$directory" ]] && [[ -f "${directory}/disc.gdi" ]]; then
#        echo "cd to: $directory" | tee -a chdman-${DATE}.log
#        cd "$directory"
#        if [[ ! -f "${directory}.chd" ]]; then
#            if chdman createcd -np 4 -i disc.gdi -o "${directory,,}.chd" | tee -a ../chdman-${DATE}.log; then
#                echo "Correct: ${directory}" >> ../chdman-${DATE}.log.ok
#            else
#                echo "Error: ${directory}" >> ../chdman-${DATE}.log.err
#            fi
#        else
#            echo "${directory}.chd Exists!... Skipping.." | tee -a ../chdman-${DATE}.log
#        fi
#        echo "cd to: .." >> ../chdman-${DATE}.log
#        cd ..
#    elif [[ -d "$directory" ]] && [[ -f "${directory}/disc.cdi" ]]; then
#        echo "Renaming: ${directory}/disc.cdi -> ${directory}/${directory,,}.cdi" | tee -a ../chdman-${DATE}.log
#        mv -v "${directory}/disc.cdi" "${directory}/${directory,,}.cdi" | tee -a ../chdman-${DATE}.log
#    fi
#done

GAMES_EXT=("cdi" "chd" "gdi")

declare -A gamearray

function get_gamearray(){
    printf '\n\tRetreiving directory listing...\n'
    SAVEIFS=$IFS
    IFS=$'\n'
    printf '\n\tGenerating gamearray\n'
    for dir in *; do
        if [[ -d "$dir" ]] && [[ -f "${dir}/name.txt" ]]; then
            gamearray["$dir"]="$(cat ""${dir}/name.txt"")"
        else
            gamearray["$dir"]="NULL"
        fi
    done
    printf '\n\t\tTotal games: %s\n' "${#gamearray[@]}"
    IFS=$SAVEIFS
}

function print_gamearray(){
    SAVEIFS=$IFS
    IFS=$'\n'
    for gamedir in ${!gamearray[@]}; do
        printf 'Dir: %s - Game: %s\n' "$gamedir" "${gamearray[$gamedir],,}"
    done
    IFS=$SAVEIFS
}

function check_dir(){
    directory="$1"
    printf '\n\tChecking directory: %s\n' "$directory"
    if ! mkdir -p "$directory"; then
        printf 'Cannot create %s... Exiting!\n' "$directory"
        return 1
    fi
    return 0
}

function move_prev_file(){
    # this thing happens because I do somethings manually :-\
    gamesrcdir="$1"
    gamename="$2"
    gameext="$3"

    dst_basedir="${DST_BASEDIR}"
    gamedstdir="${dst_basedir}/${gamesrcdir,,}"

    gamesrcfile="${gamename,,}.${gameext}"

    gamesrcpath="${gamesrcdir}/${gamesrcfile}"
    gamedstpath="${gamedstdir}/${gamesrcfile}"

    if [[ -f "$gamesrcpath" ]]; then
        printf 'Game .%s exists in origin: %s\n' "${gameext^^}" "$gamesrcfile"
        if [[ ! -f "$gamedstpath" ]]; then
            ! check_dir "$gamedstdir" && exit 1
            mv -v "$gamesrcpath" "$gamedstpath"
        fi
    fi
    if [[ -f "$gamedstpath" ]]; then
        printf 'Game exists in destination: %s\n' "$gamedstfile"
        return 0
    else
        return 1
    fi
}

function organize_files(){
    dst_basedir="${DST_BASEDIR}"
    printf '\n\tOrganizing games...\n'
    ! check_dir "$dst_basedir" && exit 1
    SAVEIFS=$IFS
    IFS=$'\n'
    for gamesrcdir in ${!gamearray[@]}; do
        gamename="${gamearray[$gamesrcdir]}"
        # I move previous chd converted files
        move_prev_file "$gamesrcdir" "$gamename" "chd"
        # I move previous cdi converted files
        move_prev_file "$gamesrcdir" "$gamename" "cdi"
    done
    IFS=$SAVEIFS
}

function main(){
    get_gamearray
    organize_files
}

main
