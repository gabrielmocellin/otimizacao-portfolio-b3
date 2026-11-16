@echo off
title Painel Streamlit - Analise de Portfolio

echo Iniciando configuracao do ambiente...

:: Se nao existir venv, cria o ambiente virtual
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativa o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Atualiza o pip e instala as dependencias
echo Instalando dependencias do requirements.txt...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Painel Streamlit rodando
echo Executando o painel Streamlit...
python -m streamlit run app.py

:: Janela aberta caso ocorra algum erro
pause
