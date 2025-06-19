from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import pyodbc

# Configuración de SQL Server (con tus datos)
SERVER = 'LAPTOP-HUI4E4B7'
DATABASE = 'EPRAN'
USERNAME = 'usuario_sql'
PASSWORD = 'abcd1234*'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # 1. Conexión a SQL Server
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={SERVER};'
            f'DATABASE={DATABASE};'
            f'UID={USERNAME};'
            f'PWD={PASSWORD}'
        )
        cursor = conn.cursor()
        
        # 2. Consulta a la tabla (con esquema dbo)
        cursor.execute('SELECT TOP(10) punto_de_interes FROM dbo.PUNTOS_INTERES')
        puntos = cursor.fetchall()
        
        # 3. Verificación y creación de botones
        if not puntos:
            await update.message.reply_text("ℹ️ No hay puntos de interés registrados.")
            return
            
        # Crear botones (uno por cada punto)
        botones = [
            [InlineKeyboardButton(punto[0], callback_data=punto[0])]
            for punto in puntos
        ]
        
        await update.message.reply_text(
            "📍 Selecciona un punto de interés:",
            reply_markup=InlineKeyboardMarkup(botones))
        
    except pyodbc.Error as e:
        await update.message.reply_text(f"❌ Error de base de datos:\n{str(e)}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error inesperado:\n{str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

async def seleccion_punto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"✅ Seleccionaste: {query.data}")

def main():
    # Token de tu bot (no lo compartas públicamente)
    TOKEN = "7525721261:AAF9vD0QEaRTiaKQdKxcUnDZF5zl-p9S1ts"
    
    # Configuración del bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(seleccion_punto))
    
    print("✅ Bot activo. Envía /start en Telegram para ver los puntos.")
    application.run_polling()

if __name__ == '__main__':
    main()