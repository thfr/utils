function fish_prompt
   set -l last_pipestatus $pipestatus
   and set retc green; or set retc red
   tty|grep -q tty; and set tty tty; or set tty pts

   set_color green
   echo -n [
   set_color normal
   if test $USER = root -o $USER = toor
      set_color red
   else
      set_color green
   end
   echo -n $USER
   set_color white
   echo -n @
   set_color normal
   if [ -z "$SSH_CLIENT" ]
      set_color green
   else
      set_color cyan
   end
   echo -n (hostname)
   set_color white
   #echo -n :(prompt_pwd)
   echo -n :(pwd|sed "s=$HOME=~=")
   set_color green
   echo -n ']'
   set_color normal
   set_color $retc
   if [ $tty = tty ]
      echo -n '-'
   else
      echo -n '─'
   end
   set_color green
   echo -n '['
   set_color normal
   set_color $retc
   echo -n (date +%X)
   set_color green
   echo -n ]
   set_color red
   printf '%s ' (__fish_git_prompt)

   # Check if acpi exists
   if not set -q __fish_nim_prompt_has_acpi
      if type acpi > /dev/null
         set -g __fish_nim_prompt_has_acpi ''
      else
         set -g __fish_nim_prompt_has_acpi '' # empty string
      end
   end

   set -l prompt_status (__fish_print_pipestatus "[" "]" "|" (set_color $fish_color_status) (set_color --bold $fish_color_status) $last_pipestatus)
   if test "$__fish_nim_prompt_has_acpi"
      if [ (acpi -a 2> /dev/null | grep off) ]
         echo -n '─['
         set_color red
         echo -n (acpi -b|cut -d' ' -f 4-)
         set_color green
         echo -n ']'
      end
   end
   echo -n $prompt_status
   echo
   set_color normal
   for job in (jobs)
      set_color brown
      echo $job
   end

   set -l prompt_status (__fish_print_pipestatus " [" "]" "|" (set_color $fish_color_status) (set_color --bold $fish_color_status) $last_pipestatus)

   set_color red
   echo -n '$ '
   set_color normal
end
