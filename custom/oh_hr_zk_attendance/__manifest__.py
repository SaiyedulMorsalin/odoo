
{
    "name": "Open HRMS Biometric Device Integration",
    "version": "18.0.1.0.0",
    "category": "Human Resources",
    "summary": "Integrate Biometric Device (Face + Thumb) with HR Attendance",
    "description": "This module integrates Odoo with the biometric device (Model: ZKteco uFace 202)",
    "author": "Bdcalling IT Ltd.",
    "maintainer": "Bdcalling IT Ltd.",
    "website": "https://www.bdcalling.com",
    "company": "Bdcalling IT Ltd.",
    "license": "AGPL-3",
    "depends": [
        "base",
        "hr_attendance"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/zk_machine_views.xml",
        "views/zk_machine_attendance_views.xml",
        "data/download_data.xml"
    ],
    "assets": {
        "web.assets_backend": [
            # Add backend JS/CSS here if needed
        ],
    },
    "images": ["static/description/banner.jpg"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
