#!/bin/bash

# Script to install frontend libraries and copy them to static/vendor

# Move to project root
PROJECT_ROOT="$(dirname "$0")"
cd "$PROJECT_ROOT" || exit 1

# Ensure npm is initialized
if [ ! -f package.json ]; then
  echo "Initializing npm..."
    npm init -y
    fi

    # Install libraries
    echo "Installing libraries via npm..."
    npm install @fortawesome/fontawesome-free leaflet chartist fullcalendar line-awesome remixicon vanillajs-datepicker

    # Create vendor folder if not exists
    VENDOR_DIR="static/vendor"
    mkdir -p "$VENDOR_DIR"

    # Copy libraries to vendor folder
    echo "Copying libraries to $VENDOR_DIR..."

    declare -A LIBS=(
      ["@fortawesome/fontawesome-free"]="fontawesome"
        ["leaflet"]="leaflet"
          ["chartist"]="chartist"
            ["fullcalendar"]="fullcalendar"
              ["line-awesome/dist"]="line-awesome"
                ["remixicon"]="remixicon"
                  ["vanillajs-datepicker"]="vanillajs-datepicker"
                  )

                  for LIB_PATH in "${!LIBS[@]}"; do
                    DEST_NAME="${LIBS[$LIB_PATH]}"
                      SRC_PATH="node_modules/$LIB_PATH"
                        
                          if [ -d "$SRC_PATH" ]; then
                              cp -r "$SRC_PATH" "$VENDOR_DIR/$DEST_NAME"
                                  echo "Copied $LIB_PATH -> $VENDOR_DIR/$DEST_NAME"
                                    else
                                        echo "Warning: $SRC_PATH not found!"
                                          fi
                                          done

                                          echo "✅ All libraries installed and copied successfully!"