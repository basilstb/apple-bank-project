from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from banking.models import UserProfile, Transaction
from decimal import Decimal

class AdminControlsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', first_name='Test', last_name='User')
        self.profile = UserProfile.objects.create(
            user=self.user,
            balance=Decimal('1000.00'),
            transaction_pin='1234',
            account_number='1234567890'
        )
        self.client.login(username='testuser', password='password123')

    def test_transfer_pending_by_default(self):
        # By default, require_pending_transactions is True
        self.assertTrue(self.profile.require_pending_transactions)
        
        # Simulate transfer session data
        session = self.client.session
        session['pending_transfer_data'] = {
            'amount': '100.00',
            'recipient_account': '9876543210',
            'account_name': 'Receiver User',
            'bank_name': 'Other Bank',
            'description': 'Test transfer'
        }
        session.save()
        
        # Verify PIN
        response = self.client.post(reverse('transfer_pin_verify'), {'pin': '1234'})
        self.assertEqual(response.status_code, 302) # Redirects to receipt
        
        # Check created transaction
        tx = Transaction.objects.latest('id')
        self.assertEqual(tx.status, 'Pending')
        self.assertEqual(tx.progress_percentage, 50)

    def test_transfer_successful_when_disabled(self):
        # Disable require_pending_transactions
        self.profile.require_pending_transactions = False
        self.profile.save()
        
        # Simulate transfer session data
        session = self.client.session
        session['pending_transfer_data'] = {
            'amount': '100.00',
            'recipient_account': '9876543210',
            'account_name': 'Receiver User',
            'bank_name': 'Other Bank',
            'description': 'Test transfer'
        }
        session.save()
        
        # Verify PIN
        response = self.client.post(reverse('transfer_pin_verify'), {'pin': '1234'})
        self.assertEqual(response.status_code, 302)
        
        # Check created transaction
        tx = Transaction.objects.latest('id')
        self.assertEqual(tx.status, 'Successful')
        self.assertEqual(tx.progress_percentage, 100)

    def test_transfer_blocked_when_allow_transfers_false(self):
        # Disable allow_transfers
        self.profile.allow_transfers = False
        self.profile.save()
        
        # Try to access transfer page
        response = self.client.get(reverse('transfer'))
        self.assertEqual(response.status_code, 302) # Redirects to dashboard
        
        # Try to access transfer PIN verify page
        response = self.client.get(reverse('transfer_pin_verify'))
        self.assertEqual(response.status_code, 302) # Redirects to dashboard

    def test_admin_transaction_changelist(self):
        admin_user = User.objects.create_superuser(username='adminuser', password='adminpassword', email='admin@test.com')
        admin_client = Client()
        admin_client.login(username='adminuser', password='adminpassword')
        Transaction.objects.create(
            sender=self.profile,
            amount=Decimal('50.00'),
            description='Test TX',
            transaction_type='Transfer',
            status='Successful',
            progress_percentage=100
        )
        response = admin_client.get('/secure-admin-portal/banking/transaction/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Set selected transactions to Pending (50%)')
        self.assertContains(response, 'Set selected transactions to Successful (100%)')

    def test_dashboard_displays_suspension_reason_when_suspended(self):
        self.profile.account_status = 'Suspended'
        self.profile.suspension_reason = 'Account suspended pending KYC document verification.'
        self.profile.save()

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Access Restricted (Suspended)')
        self.assertContains(response, 'Account suspended pending KYC document verification.')
        self.assertContains(response, 'Reason for Suspension:')

    def test_transfer_blocked_when_account_suspended(self):
        self.profile.account_status = 'Suspended'
        self.profile.suspension_reason = 'Fraud check in progress.'
        self.profile.save()

        response = self.client.get(reverse('transfer'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your account is suspended: Fraud check in progress.')

    def test_admin_suspend_account_view(self):
        admin_user = User.objects.create_superuser(username='admin2', password='adminpassword2', email='admin2@test.com')
        admin_client = Client()
        admin_client.login(username='admin2', password='adminpassword2')

        # Suspend user with custom reason
        suspend_url = reverse('admin:user_suspend_account', args=[self.user.pk])
        response = admin_client.post(suspend_url, {
            'action_type': 'suspend',
            'reason': 'Suspicious IP login detected.'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.account_status, 'Suspended')
        self.assertEqual(self.profile.suspension_reason, 'Suspicious IP login detected.')

        # Reactivate user
        response = admin_client.post(suspend_url, {
            'action_type': 'activate'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.account_status, 'Active')
        self.assertIsNone(self.profile.suspension_reason)


