import cv2
import pyvirtualcam


def check_virtual_camera_backends():
    """Check if virtual camera backends are available by attempting to create a test camera."""
    print("Checking virtual camera backend availability...")

    try:
        # Try to create a minimal virtual camera to test if backends are available
        with pyvirtualcam.Camera(width=640, height=480, fps=30) as test_cam:
            print(f"Virtual camera backend working: {test_cam.device}")
            return True
    except RuntimeError as e:
        print(f"Virtual camera backend not available: {e}")
        print_installation_guide()
        return False
    except (OSError, ImportError) as e:
        print(f"Error checking backends: {e}")
        print_installation_guide()
        return False


def print_installation_guide():
    """Print installation guide for virtual camera backends."""
    print("\n" + "="*60)
    print("VIRTUAL CAMERA SETUP REQUIRED")
    print("="*60)
    print("\nTo use this application, you need to install a virtual camera backend:")
    print("\n🎯 RECOMMENDED - OBS Studio:")
    print("  1. Download and install OBS Studio from: https://obsproject.com/")
    print("  2. Start OBS Studio at least once")
    print("  3. The OBS Virtual Camera will be automatically available")
    print("  ✅ Most reliable and widely supported option")
    print("\n⚠️  Alternative - Unity Capture (Not Recommended):")
    print("  1. Download Unity Capture from: https://github.com/schellingb/UnityCapture")
    print("  2. Run the installer as administrator")
    print("  3. Register the virtual camera device")
    print("  ⚠️  Note: Older software with limited compatibility")
    print("\nAfter installation, restart this application.")
    print("="*60)


def demo_mode():
    """Run in demo mode without virtual camera - shows processed video only."""
    print("\n" + "="*50)
    print("RUNNING IN DEMO MODE")
    print("="*50)
    print("Virtual camera not available, showing preview only.")
    print("This demonstrates the image processing without virtual camera output.")
    print("Press 'q' to exit.")
    print("="*50)

    # Open the physical webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open webcam for demo mode.")
        return

    try:
        while True:
            # Capture frame from webcam
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Apply the same processing as the main application
            manipulated_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            manipulated_frame = cv2.cvtColor(
                manipulated_frame, cv2.COLOR_GRAY2BGR)

            # Display both original and processed frames
            cv2.imshow('Original Feed', frame)
            cv2.imshow('Processed Feed (Grayscale)', manipulated_frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Demo mode ended.")


def main():
    print("WebcamWrapper - Virtual Camera Application")
    print("-" * 40)

    # Check if virtual camera backends are available
    if not check_virtual_camera_backends():
        response = input(
            "\nWould you like to run in demo mode instead? (y/n): ").lower().strip()
        if response == 'y' or response == 'yes':
            demo_mode()
        return

    # Open the physical webcam (index 0 is usually the default webcam)
    # Use DirectShow for better Windows compatibility
    print("Initializing physical webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        print("Please check that:")
        print("  - Your webcam is connected and working")
        print("  - No other applications are using the webcam")
        print("  - Windows has permission to access the camera")
        return

    # Get webcam properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS if not detected

    print(f"Physical webcam initialized: {width}x{height} @ {fps} FPS")

    # Create virtual camera with enhanced error handling
    try:
        print("Creating virtual camera...")
        with pyvirtualcam.Camera(width=width, height=height, fps=fps, fmt=pyvirtualcam.PixelFormat.BGR) as cam:
            print(
                f"Virtual camera started: {cam.device} ({width}x{height} @ {fps} FPS)")
            print("Press 'q' in the preview window to exit")

            while True:
                # Capture frame from webcam
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break

                # Example manipulation: Convert frame to grayscale
                manipulated_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Convert back to BGR for virtual camera (which expects 3 channels)
                manipulated_frame = cv2.cvtColor(
                    manipulated_frame, cv2.COLOR_GRAY2BGR)

                # Send manipulated frame to virtual camera
                cam.send(manipulated_frame)

                # Update the virtual camera (maintain FPS)
                cam.sleep_until_next_frame()

                # Optional: Display the manipulated frame for debugging
                cv2.imshow('Virtual Camera Output', manipulated_frame)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except RuntimeError as e:
        print(f"\nError creating virtual camera: {e}")
        print_installation_guide()
        return
    except (OSError, ImportError) as e:
        print(f"\nUnexpected error: {e}")
        return
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        print("Cleanup completed.")


if __name__ == "__main__":
    main()
