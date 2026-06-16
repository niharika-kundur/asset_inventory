# Asset Inventory Tool

A simple Django-based asset tracking application.

## Features

- **User Authentication** - Login, Logout, Change Password
- **Role-Based Access**
  - Superuser: View all assets, Add, Transfer, Delete, View History
  - Normal User: View only assigned assets, Add assets (auto-assigned to self)
- **Asset Management**
  - Add new assets with assigned date tracking
  - View asset list with filters
  - Transfer assets between users (Superuser only)
  - Delete assets with confirmation modal (Superuser only)
- **Search** - Search assets by Asset ID
- **Filter** - Filter assets by Status and Assigned Date
- **Date Filtering** - Filter by specific date or date range
- **Export to CSV** - Download asset list as CSV file
- **Audit History** - Track all changes made to assets (Superuser only)

## Technologies Used

| Technology  | Purpose                  |
|-------------|--------------------------|
| Django 6.x  | Web framework            |
| SQLite      | Database                 |
| Bootstrap 5 | UI styling               |
| HTML/CSS    | Templates                |
| JavaScript  | Date filter toggle       |

## Project Structure

```
inventory/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── inventory_project/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── assets/                 # Main app
    ├── models.py           # Asset & AssetHistory models
    ├── views.py            # Business logic
    ├── urls.py             # URL routing
    ├── admin.py            # Admin registration
    └── templates/          # HTML templates
        ├── base.html
        ├── home.html
        ├── login.html
        ├── asset_list.html
        ├── add_asset.html
        ├── edit_asset.html
        ├── asset_history.html
        ├── change_password.html
        └── change_password_done.html
```

## How to Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

4. Start the server:
   ```
   python manage.py runserver
   ```

5. Open browser: http://127.0.0.1:8000/

## URLs

| URL                 | Description            |
|---------------------|------------------------|
| `/`                 | Home page              |
| `/login/`           | Login page             |
| `/logout/`          | Logout                 |
| `/assets/`          | Asset list             |
| `/add/`             | Add new asset          |
| `/edit/<id>/`       | Transfer asset         |
| `/delete/<id>/`     | Delete asset           |
| `/history/<id>/`    | View asset history     |
| `/assets/export/`   | Export to CSV          |
| `/change-password/` | Change password        |
| `/admin/`           | Django admin panel     |

## User Roles

| Feature            | Superuser            | Normal User               |
|--------------------|----------------------|---------------------------|
| View all assets    | ✅                   | ❌                        |
| View own assets    | ✅                   | ✅                        |
| Add asset          | ✅ (assign to anyone)| ✅ (auto-assigned to self)|
| Transfer asset     | ✅                   | ❌                        |
| Delete asset       | ✅                   | ❌                        |
| Export CSV         | ✅ (all assets)      | ✅ (own assets only)      |
| View audit history | ✅                   | ❌                        |
| Date filtering     | ✅                   | ✅                        |

## Pages Overview

### Asset List Page
- Table with S.No, Asset ID, Name, Type, Assigned To, Assigned Date, Status
- Search by Asset ID
- Filter by Status (dropdown)
- Filter by Assigned Date (On specific date / Between dates)
- Export to CSV button
- History, Transfer, and Delete buttons (Superuser only)

### Add Asset Page
- Form with Asset ID, Name, Type, Assigned To, Status
- Duplicate Asset ID validation
- Assigned date automatically set to current date

### Asset History Page (Superuser Only)
- Shows complete audit trail of an asset
- Tracks: Created, Transferred, Updated changes
- Displays: Who changed, What changed, When, Old/New values

## Database Models

### Asset
| Field         | Type      | Description                    |
|---------------|-----------|--------------------------------|
| asset_id      | CharField | Unique identifier              |
| asset_name    | CharField | Name of the asset              |
| asset_type    | CharField | Type (Laptop, Monitor, etc.)   |
| assigned_to   | CharField | Username of assigned person    |
| status        | CharField | Available, In Use, Under Repair|
| assigned_date | DateField | Date when asset was assigned   |

### AssetHistory
| Field         | Type          | Description                    |
|---------------|---------------|--------------------------------|
| asset         | ForeignKey    | Link to Asset                  |
| changed_by    | CharField     | Who made the change            |
| change_type   | CharField     | Created, Transferred, Updated  |
| field_changed | CharField     | Which field was modified       |
| old_value     | CharField     | Previous value                 |
| new_value     | CharField     | New value                      |
| changed_at    | DateTimeField | When the change occurred       |
| notes         | TextField     | Additional details             |

---

*Developed as part of Django learning and skill development.*
