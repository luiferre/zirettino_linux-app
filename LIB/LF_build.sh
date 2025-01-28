#!/bin/bash

# Variabili di configurazione
CXX=g++
CXXFLAGS="-std=c++14 -fPIC -I./ -I/home/utente/projects/LIB/boost/boost -fno-stack-protector"
LDFLAGS="-shared"
OUTPUT_LIB="../lib_zire.so"
BUILD_DIR="./build"
SOURCE_FILES=("zire_dll.cpp" "zire_class.cpp" "ZIRE_DATAHANDLER.cpp" "ZIRE_HAL.cpp")

# Creazione della directory di build
mkdir -p $BUILD_DIR

echo "Compilazione dei file sorgente in oggetti..."

# Compilazione dei file sorgente in oggetti
for src_file in "${SOURCE_FILES[@]}"; do
    obj_file="$BUILD_DIR/$(basename $src_file .cpp).o"
    echo "Compilando $src_file -> $obj_file"
    $CXX $CXXFLAGS -c $src_file -o $obj_file
    if [ $? -ne 0 ]; then
        echo "Errore durante la compilazione di $src_file"
        exit 1
    fi
done

echo "Creazione della libreria dinamica $OUTPUT_LIB..."

# Creazione della libreria dinamica
OBJ_FILES=$(find $BUILD_DIR -name "*.o")
$CXX $LDFLAGS $OBJ_FILES -o $OUTPUT_LIB
if [ $? -ne 0 ]; then
    echo "Errore durante la creazione della libreria dinamica"
    exit 1
fi

echo "Libreria dinamica creata con successo: $OUTPUT_LIB"

# Pulizia opzionale (commenta questa sezione per mantenere i file oggetto)
echo "Pulizia dei file oggetto..."
rm -rf $BUILD_DIR

echo "Script completato con successo!"
