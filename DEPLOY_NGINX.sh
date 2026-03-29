#!/bin/bash
# ============================================================
# MWECAU DigiVote - Nginx + Gunicorn Deployment
# ============================================================

echo "🚀 Configuring Nginx + Gunicorn for DigiVote..."
echo "================================================="
echo ""

# Stop any existing Gunicorn on port 81
echo "🛑 Stopping existing processes..."
PID=$(sudo lsof -ti :81)
if [ ! -z "$PID" ]; then
    sudo kill $PID
    echo "   Killed process on port 81"
fi

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p /var/www/mwecau_digivote/logs

# Set proper permissions
echo "🔐 Setting permissions..."
sudo chown -R www-data:www-data /var/www/mwecau_digivote
sudo chmod -R 755 /var/www/mwecau_digivote

# Copy systemd service file
echo "⚙️  Installing Gunicorn service..."
sudo cp /var/www/mwecau_digivote/digivote.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable digivote
sudo systemctl start digivote

# Copy Nginx configuration
echo "🌐 Configuring Nginx..."
sudo cp /var/www/mwecau_digivote/nginx-digivote.conf /etc/nginx/sites-available/digivote
sudo ln -sf /etc/nginx/sites-available/digivote /etc/nginx/sites-enabled/digivote
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "✅ Deployment Complete!"
echo "================================================="
echo "🌐 Access: http://159.65.119.182:81"
echo ""
echo "📊 Service Status:"
sudo systemctl status digivote --no-pager -l
echo ""
echo "🔧 Useful Commands:"
echo "   sudo systemctl status digivote    # Check status"
echo "   sudo systemctl restart digivote   # Restart service"
echo "   sudo journalctl -u digivote -f    # View logs"
echo "   sudo systemctl reload nginx       # Reload Nginx"
