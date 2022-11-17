from datetime import datetime
from unittest import mock

from freezegun import freeze_time

from providers.aws.services.directoryservice.directoryservice_service import (
    Certificate,
    CertificateState,
    CertificateType,
    Directory,
)

AWS_REGION = "eu-west-1"


# Always use a mocked date to test the certificates expiration
@freeze_time("2023-01-01")
class Test_directoryservice_ldap_certificate_expiration:
    def test_no_directories(self):
        directoryservice_client = mock.MagicMock
        directoryservice_client.directories = {}
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_ldap_certificate_expiration.directoryservice_ldap_certificate_expiration import (
                directoryservice_ldap_certificate_expiration,
            )

            check = directoryservice_ldap_certificate_expiration()
            result = check.execute()

            assert len(result) == 0

    def test_directory_no_certificate(self):
        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                certificates=[],
            )
        }
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_ldap_certificate_expiration.directoryservice_ldap_certificate_expiration import (
                directoryservice_ldap_certificate_expiration,
            )

            check = directoryservice_ldap_certificate_expiration()
            result = check.execute()

            assert len(result) == 0

    def test_directory_certificate_expires_in_365_days(self):
        remaining_days_to_expire = 365

        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        certificate_id = "test-certificate"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                certificates=[
                    Certificate(
                        id=certificate_id,
                        common_name=certificate_id,
                        state=CertificateState.Registered,
                        type=CertificateType.ClientLDAPS,
                        expiry_date_time=datetime(2024, 1, 1),
                    )
                ],
            )
        }

        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_ldap_certificate_expiration.directoryservice_ldap_certificate_expiration import (
                directoryservice_ldap_certificate_expiration,
            )

            check = directoryservice_ldap_certificate_expiration()
            result = check.execute()

            assert len(result) == 1
            assert result[0].resource_id == certificate_id
            assert result[0].region == AWS_REGION
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"LDAP Certificate {certificate_id} configured at {directory_name} expires in {remaining_days_to_expire} days"
            )

    def test_directory_certificate_expires_in_90_days(self):
        remaining_days_to_expire = 90

        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        certificate_id = "test-certificate"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                certificates=[
                    Certificate(
                        id=certificate_id,
                        common_name=certificate_id,
                        state=CertificateState.Registered,
                        type=CertificateType.ClientLDAPS,
                        expiry_date_time=datetime(2023, 4, 1),
                    )
                ],
            )
        }

        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_ldap_certificate_expiration.directoryservice_ldap_certificate_expiration import (
                directoryservice_ldap_certificate_expiration,
            )

            check = directoryservice_ldap_certificate_expiration()
            result = check.execute()

            assert len(result) == 1
            assert result[0].resource_id == certificate_id
            assert result[0].region == AWS_REGION
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"LDAP Certificate {certificate_id} configured at {directory_name} is about to expire in {remaining_days_to_expire} days"
            )

    def test_directory_certificate_expires_in_31_days(self):
        remaining_days_to_expire = 31

        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        certificate_id = "test-certificate"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                certificates=[
                    Certificate(
                        id=certificate_id,
                        common_name=certificate_id,
                        state=CertificateState.Registered,
                        type=CertificateType.ClientLDAPS,
                        expiry_date_time=datetime(2023, 2, 1),
                    )
                ],
            )
        }

        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_ldap_certificate_expiration.directoryservice_ldap_certificate_expiration import (
                directoryservice_ldap_certificate_expiration,
            )

            check = directoryservice_ldap_certificate_expiration()
            result = check.execute()

            assert len(result) == 1
            assert result[0].resource_id == certificate_id
            assert result[0].region == AWS_REGION
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"LDAP Certificate {certificate_id} configured at {directory_name} is about to expire in {remaining_days_to_expire} days"
            )