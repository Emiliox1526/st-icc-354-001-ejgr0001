#!/usr/bin/env python3
import argparse
import requests

BASE_URL = "http://localhost:7070"  # Asegúrate de que coincida con la configuración de tu servidor

def register_user(username, password):
    endpoint = f"{BASE_URL}/register"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(endpoint, data=data)
    if response.status_code == 201:
        print("¡Usuario registrado exitosamente!")
    else:
        print("Error al registrar:", response.text)

def login(username, password):
    endpoint = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(endpoint, data=data)
    if response.status_code == 200:
        token = response.json().get("token")
        print("¡Login exitoso!")
        print("Token JWT:", token)
        return token
    else:
        print("Error en login:", response.text)
        return None

def shorten_url(url, token):
    endpoint = f"{BASE_URL}/shorten"
    data = {"url": url}
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.post(endpoint, data=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print("URL acortada exitosamente:")
        print("Short URL:", result.get("shortUrl"))
        return result
    else:
        print("Error al acortar la URL:", response.text)
        return None

def get_url_summary(short_code, token):
    endpoint = f"{BASE_URL}/api/summary/{short_code}"
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        summary = response.json()
        print("Resumen del enlace:")
        print(summary)
        return summary
    else:
        print("Error al obtener el resumen:", response.text)
        return None

def main():
    parser = argparse.ArgumentParser(description="Cliente REST para el URL Shortener")
    subparsers = parser.add_subparsers(dest="command", help="Acciones: register, login, shorten, summary")

    # Registro
    parser_register = subparsers.add_parser("register", help="Registrar un nuevo usuario")
    parser_register.add_argument("--username", required=True, help="Nombre de usuario")
    parser_register.add_argument("--password", required=True, help="Contraseña")

    # Login
    parser_login = subparsers.add_parser("login", help="Iniciar sesión y obtener token")
    parser_login.add_argument("--username", required=True, help="Nombre de usuario")
    parser_login.add_argument("--password", required=True, help="Contraseña")

    # Acortar URL
    parser_shorten = subparsers.add_parser("shorten", help="Acortar una URL")
    parser_shorten.add_argument("--url", required=True, help="La URL a acortar")
    parser_shorten.add_argument("--token", required=True, help="Token JWT obtenido en el login")

    # Obtener resumen
    parser_summary = subparsers.add_parser("summary", help="Obtener resumen de una URL acortada")
    parser_summary.add_argument("--shortcode", required=True, help="Código corto de la URL")
    parser_summary.add_argument("--token", required=True, help="Token JWT obtenido en el login")

    args = parser.parse_args()

    if args.command == "register":
        register_user(args.username, args.password)
    elif args.command == "login":
        login(args.username, args.password)
    elif args.command == "shorten":
        shorten_url(args.url, args.token)
    elif args.command == "summary":
        get_url_summary(args.shortcode, args.token)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
